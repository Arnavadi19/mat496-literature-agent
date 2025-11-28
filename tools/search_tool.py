"""
Web search tool implementation.

Supports multiple search backends:
- Brave Search API
- SerpAPI (Google)
- DuckDuckGo (free fallback)
"""

from typing import List, Dict
import os


def search_brave(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search using Brave Search API.
    
    TODO: Install brave-search-python
    TODO: Get API key from https://brave.com/search/api/
    TODO: Set BRAVE_API_KEY environment variable
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of dicts with 'title', 'url', 'snippet'
    """
    # TODO: from brave import Brave
    # brave = Brave(api_key=os.getenv("BRAVE_API_KEY"))
    # results = brave.search(q=query, count=num_results)
    # return [{"title": r.title, "url": r.url, "snippet": r.description} 
    #         for r in results.web_results]
    
    # Placeholder
    return [
        {
            "title": f"Result {i+1} for {query}",
            "url": f"https://example.com/result{i+1}",
            "snippet": f"Snippet for result {i+1}"
        }
        for i in range(num_results)
    ]


def search_serp(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search using SerpAPI (Google Search).
    
    TODO: Install google-search-results
    TODO: Get API key from https://serpapi.com/
    TODO: Set SERPAPI_KEY environment variable
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of dicts with 'title', 'url', 'snippet'
    """
    # TODO: from serpapi import GoogleSearch
    # params = {
    #     "q": query,
    #     "num": num_results,
    #     "api_key": os.getenv("SERPAPI_KEY")
    # }
    # search = GoogleSearch(params)
    # results = search.get_dict()
    # return [{"title": r["title"], "url": r["link"], "snippet": r.get("snippet", "")}
    #         for r in results.get("organic_results", [])]
    
    # Placeholder
    return search_brave(query, num_results)


def search_web(query: str, backend: str = "brave", num_results: int = 5) -> List[Dict[str, str]]:
    """
    Unified search interface.
    
    Args:
        query: Search query
        backend: 'brave' or 'serp'
        num_results: Number of results
        
    Returns:
        Search results
    """
    if backend == "brave":
        return search_brave(query, num_results)
    elif backend == "serp":
        return search_serp(query, num_results)
    else:
        raise ValueError(f"Unknown backend: {backend}")
