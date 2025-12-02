"""
Caching utilities for search results and embeddings.

This module provides a simple file-based cache to avoid redundant API calls
and reduce costs during development and repeated runs.
"""

import os
import json
import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, List


CACHE_DIR = Path(".cache")
CACHE_EXPIRY_HOURS = 24  # Cache expires after 24 hours


def _get_cache_path(cache_type: str, key: str) -> Path:
    """Get the cache file path for a given key."""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_subdir = CACHE_DIR / cache_type
    cache_subdir.mkdir(exist_ok=True)
    
    # Hash the key to create a safe filename
    key_hash = hashlib.md5(key.encode()).hexdigest()
    return cache_subdir / f"{key_hash}.pkl"


def _is_cache_valid(cache_path: Path) -> bool:
    """Check if cache file exists and is not expired."""
    if not cache_path.exists():
        return False
    
    # Check if file is older than expiry time
    file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
    expiry_time = datetime.now() - timedelta(hours=CACHE_EXPIRY_HOURS)
    
    return file_time > expiry_time


def get_cached_search(query: str) -> Optional[List[Dict]]:
    """
    Get cached search results for a query.
    
    Args:
        query: Search query string
        
    Returns:
        Cached search results or None if not found/expired
    """
    cache_path = _get_cache_path("search", query)
    
    if _is_cache_valid(cache_path):
        try:
            with open(cache_path, 'rb') as f:
                cached_data = pickle.load(f)
            print(f"  Using cached search results for: {query[:50]}...")
            return cached_data
        except Exception as e:
            print(f"  Warning: Failed to load cache: {e}")
            return None
    
    return None


def cache_search_results(query: str, results: List[Dict]) -> None:
    """
    Cache search results for a query.
    
    Args:
        query: Search query string
        results: Search results to cache
    """
    cache_path = _get_cache_path("search", query)
    
    try:
        with open(cache_path, 'wb') as f:
            pickle.dump(results, f)
        print(f"  Cached search results for: {query[:50]}...")
    except Exception as e:
        print(f"  Warning: Failed to cache results: {e}")


def get_cached_embeddings(doc_hash: str) -> Optional[Any]:
    """
    Get cached embeddings for a document.
    
    Args:
        doc_hash: Hash of the document content
        
    Returns:
        Cached embeddings or None if not found/expired
    """
    cache_path = _get_cache_path("embeddings", doc_hash)
    
    if _is_cache_valid(cache_path):
        try:
            with open(cache_path, 'rb') as f:
                cached_embeddings = pickle.load(f)
            return cached_embeddings
        except Exception:
            return None
    
    return None


def cache_embeddings(doc_hash: str, embeddings: Any) -> None:
    """
    Cache embeddings for a document.
    
    Args:
        doc_hash: Hash of the document content
        embeddings: Embeddings to cache
    """
    cache_path = _get_cache_path("embeddings", doc_hash)
    
    try:
        with open(cache_path, 'wb') as f:
            pickle.dump(embeddings, f)
    except Exception as e:
        print(f"  Warning: Failed to cache embeddings: {e}")


def clear_cache(cache_type: Optional[str] = None) -> None:
    """
    Clear cache files.
    
    Args:
        cache_type: Type of cache to clear ('search', 'embeddings', or None for all)
    """
    if cache_type:
        cache_subdir = CACHE_DIR / cache_type
        if cache_subdir.exists():
            for file in cache_subdir.glob("*.pkl"):
                file.unlink()
            print(f"Cleared {cache_type} cache")
    else:
        if CACHE_DIR.exists():
            for file in CACHE_DIR.glob("**/*.pkl"):
                file.unlink()
            print("Cleared all cache")


def get_cache_stats() -> Dict[str, int]:
    """Get statistics about cache usage."""
    stats = {"search": 0, "embeddings": 0}
    
    for cache_type in stats.keys():
        cache_subdir = CACHE_DIR / cache_type
        if cache_subdir.exists():
            stats[cache_type] = len(list(cache_subdir.glob("*.pkl")))
    
    return stats
