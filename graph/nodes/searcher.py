"""
Searcher node: Executes web searches for each subtopic.
"""

from typing import List, Dict
from graph.state import ReviewState


def search_web(state: ReviewState) -> ReviewState:
    """
    For each subtopic, calls search tool to obtain URLs using DuckDuckGo (FREE).
    
    Uses DuckDuckGo search which requires no API keys or credit cards.
    Falls back to placeholder URLs if search fails.
    
    Args:
        state: Current ReviewState with subtopics
        
    Returns:
        Updated ReviewState with search_results (URLs) added to state
    """
    print(f"[SEARCHER] Searching web for {len(state['subtopics'])} subtopics")
    
    # Import the free search tool
    from tools.search_tool import search_web as perform_search
    
    search_results: Dict[str, List[str]] = {}
    
    for subtopic in state["subtopics"]:
        print(f"  Searching: {subtopic.search_query}")
        
        try:
            # Use DuckDuckGo search (free, no API key needed)
            results = perform_search(subtopic.search_query, backend="duckduckgo", num_results=5)
            
            # Extract URLs from search results
            urls = [r["url"] for r in results if r.get("url")]
            
            # Filter out non-http URLs (keep both http and https)
            valid_urls = [url for url in urls if url.startswith("http")]
            
            search_results[subtopic.name] = valid_urls[:5]  # Top 5 URLs
            print(f"    Found {len(valid_urls)} valid URLs")
            
        except Exception as e:
            print(f"    Warning: Search failed: {e}. Using placeholder.")
            # Fallback to placeholder URLs
            search_results[subtopic.name] = [
                f"https://example.com/article1-{subtopic.name}",
                f"https://example.com/article2-{subtopic.name}",
                f"https://example.com/article3-{subtopic.name}",
            ]
    
    # Debug: Log total URLs found
    total_urls = sum(len(urls) for urls in search_results.values())
    print(f"  Total URLs collected: {total_urls}")
    
    # Store results in state
    state["_search_results"] = search_results  # type: ignore
    
    return state
