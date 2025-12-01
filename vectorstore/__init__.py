"""
Vector store utilities for semantic search.

This module contains FAISS initialization and helper functions for
persistence, loading, and management of vector stores.
"""

from pathlib import Path
from typing import Optional
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def save_vector_store(vector_store: FAISS, path: str) -> None:
    """
    Saves a FAISS vector store to disk.
    
    Args:
        vector_store: FAISS vector store instance
        path: Directory path to save the index
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(path)
    print(f"✓ Vector store saved to {path}")


def load_vector_store(path: str, embeddings: Optional[OpenAIEmbeddings] = None) -> Optional[FAISS]:
    """
    Loads a FAISS vector store from disk.
    
    Args:
        path: Directory path where the index is saved
        embeddings: Embeddings instance (if None, creates new OpenAIEmbeddings)
        
    Returns:
        Loaded FAISS vector store or None if load fails
    """
    try:
        if embeddings is None:
            embeddings = OpenAIEmbeddings()
        
        vector_store = FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True  # Required for FAISS
        )
        print(f"✓ Vector store loaded from {path}")
        return vector_store
    except Exception as e:
        print(f"⚠️  Failed to load vector store from {path}: {e}")
        return None


def merge_vector_stores(store1: FAISS, store2: FAISS) -> FAISS:
    """
    Merges two FAISS vector stores.
    
    Args:
        store1: First vector store
        store2: Second vector store
        
    Returns:
        Merged vector store
    """
    store1.merge_from(store2)
    return store1
