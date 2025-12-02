"""
Fetcher node: Fetches webpage content for collected URLs.
"""

from typing import List
from graph.state import ReviewState, Document
from tools.fetch_tool import fetch_url


def fetch_pages(state: ReviewState) -> ReviewState:
    """
    Fetches HTML content from URLs and extracts text.
    
    Uses the fetch_tool to scrape actual web content.
    Handles errors gracefully with placeholder content.
    
    Args:
        state: ReviewState with search results
        
    Returns:
        Updated ReviewState with documents populated
    """
    print("[FETCHER] Fetching webpage content")
    
    documents: List[Document] = []
    search_results = state.get("_search_results", {})
    
    # Debug: Log what we received
    total_urls = sum(len(urls) for urls in search_results.values())
    print(f"  Received {total_urls} URLs to fetch from {len(search_results)} subtopics")
    
    for subtopic_name, urls in search_results.items():
        print(f"  Fetching {len(urls)} URLs for: {subtopic_name}")
        
        for url in urls:
            try:
                # Fetch actual content
                content = fetch_url(url, timeout=10)
                
                if content:
                    # Create document with actual content
                    documents.append(
                        Document(
                            url=url,
                            title=f"Article about {subtopic_name}",
                            content=content[:10000],  # Limit to 10k chars to avoid token limits
                            subtopic=subtopic_name
                        )
                    )
                    print(f"    Fetched {len(content)} chars from {url[:50]}...")
                else:
                    # Fallback to placeholder if fetch fails
                    print(f"    Warning: Failed to fetch {url[:50]}... Using placeholder")
                    documents.append(_create_placeholder_doc(url, subtopic_name))
                    
            except Exception as e:
                print(f"    Warning: Error fetching {url[:50]}...: {e}")
                documents.append(_create_placeholder_doc(url, subtopic_name))
    
    print(f"  Total documents fetched: {len(documents)}")
    state["documents"] = documents
    return state


def _create_placeholder_doc(url: str, subtopic: str) -> Document:
    """Creates placeholder document when fetch fails."""
    return Document(
        url=url,
        title=f"Placeholder for {subtopic}",
        content=f"Placeholder content for {url}. This would contain actual scraped text in production.",
        subtopic=subtopic
    )
