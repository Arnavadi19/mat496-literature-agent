"""
Searcher node: Executes web searches for each subtopic.
"""

from typing import List, Dict
from graph.state import ReviewState


def search_web(state: ReviewState) -> ReviewState:
    """
    For each subtopic, calls search tool to obtain URLs.
    
    TODO: Integrate with Brave Search API or SerpAPI
    TODO: Import and use tools.search_tool
    
    Args:
        state: Current ReviewState with subtopics
        
    Returns:
        Updated ReviewState with search_results (URLs) added to state
    """
    print(f"[SEARCHER] Searching web for {len(state['subtopics'])} subtopics")
    
    # TODO: Import from tools.search_tool import search_brave
    # TODO: For each subtopic, call search API
    # TODO: Collect top 3-5 URLs per subtopic
    
    # Placeholder: Add URLs to state metadata
    # In real implementation, store URLs associated with each subtopic
    search_results: Dict[str, List[str]] = {}
    
    for subtopic in state["subtopics"]:
        # Placeholder URLs
        search_results[subtopic.name] = [
            f"https://example.com/article1-{subtopic.name}",
            f"https://example.com/article2-{subtopic.name}",
            f"https://example.com/article3-{subtopic.name}",
        ]
    
    # Store results in state (you may want to add search_results to ReviewState)
    # For now, we'll pass it forward via documents in the next node
    state["_search_results"] = search_results  # type: ignore
    
    return state
