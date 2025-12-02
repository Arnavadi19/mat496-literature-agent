"""
Web search tool implementation.

Uses DuckDuckGo search - completely FREE, no API key required!

For production use, you can optionally integrate:
- SerpAPI (requires API key, paid)
- Brave Search API (requires API key, has free tier)
"""

from typing import List, Dict, Optional


def search_duckduckgo(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search using DuckDuckGo (FREE - no API key required).
    
    Uses the ddgs library which is completely free
    and doesn't require any API keys or credit cards.
    
    Installation:
        pip install ddgs
    
    Args:
        query: Search query (simple keywords work best)
        num_results: Number of results to return (default: 5)
        
    Returns:
        List of dicts with 'title', 'url', 'snippet'
    """
    try:
        from ddgs import DDGS
        
        results = []
        ddgs = DDGS()
        
        # Use text search
        search_results = list(ddgs.text(query, max_results=num_results))
        
        for r in search_results:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        
        return results
        
    except ImportError:
        print("Warning: ddgs not installed. Install with: pip install ddgs")
        print("   Using placeholder results for now.")
        # Return placeholder results if library not installed
        return [
            {
                "title": f"Result {i+1} for {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"Placeholder snippet for result {i+1}. Install ddgs to get real results."
            }
            for i in range(num_results)
        ]
    except Exception as e:
        print(f"Error during search: {e}")
        return []


def search_serp(query: str, num_results: int = 5, api_key: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Search using SerpAPI (Google Search) - PAID service.
    
    Optional integration for production use.
    Requires API key from https://serpapi.com/
    
    Args:
        query: Search query
        num_results: Number of results to return
        api_key: SerpAPI key (or set SERPAPI_KEY environment variable)
        
    Returns:
        List of dicts with 'title', 'url', 'snippet'
    """
    try:
        from serpapi import GoogleSearch
        import os
        
        key = api_key or os.getenv("SERPAPI_KEY")
        if not key:
            print("Warning: SERPAPI_KEY not set. Falling back to DuckDuckGo.")
            return search_duckduckgo(query, num_results)
        
        params = {
            "q": query,
            "num": num_results,
            "api_key": key
        }
        search = GoogleSearch(params)
        results_dict = search.get_dict()
        
        return [
            {
                "title": r["title"],
                "url": r["link"],
                "snippet": r.get("snippet", "")
            }
            for r in results_dict.get("organic_results", [])
        ]
        
    except ImportError:
        print("Warning: google-search-results not installed. Falling back to DuckDuckGo.")
        return search_duckduckgo(query, num_results)
    except Exception as e:
        print(f"SerpAPI error: {e}. Falling back to DuckDuckGo.")
        return search_duckduckgo(query, num_results)


def search_web(query: str, backend: str = "duckduckgo", num_results: int = 5) -> List[Dict[str, str]]:
    """
    Unified search interface with automatic fallback.
    
    Default backend is DuckDuckGo (free, no API key needed).
    
    Args:
        query: Search query
        backend: 'duckduckgo' (default, free) or 'serp' (paid)
        num_results: Number of results to return
        
    Returns:
        Search results as list of dicts with title, url, snippet
        
    Example:
        >>> results = search_web("Python programming", num_results=3)
        >>> for r in results:
        ...     print(f"{r['title']}: {r['url']}")
    """
    if backend == "duckduckgo":
        return search_duckduckgo(query, num_results)
    elif backend == "serp":
        return search_serp(query, num_results)
    else:
        print(f"Warning: Unknown backend '{backend}'. Using DuckDuckGo.")
        return search_duckduckgo(query, num_results)
