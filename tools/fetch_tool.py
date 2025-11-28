"""
Web page fetching and content extraction tool.
"""

from typing import Optional
import requests
from bs4 import BeautifulSoup


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """
    Fetches a URL and extracts main text content.
    
    TODO: Add better content extraction (newspaper3k or trafilatura)
    TODO: Add error handling and retries
    TODO: Add rate limiting
    TODO: Handle different content types (PDF, etc.)
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Extracted text content, or None if failed
    """
    try:
        # TODO: Consider using trafilatura for better extraction
        # from trafilatura import fetch_url, extract
        # downloaded = fetch_url(url)
        # text = extract(downloaded)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_multiple(urls: list[str], max_workers: int = 5) -> dict[str, Optional[str]]:
    """
    Fetches multiple URLs concurrently.
    
    TODO: Implement concurrent fetching with ThreadPoolExecutor
    TODO: Add progress tracking
    
    Args:
        urls: List of URLs to fetch
        max_workers: Maximum concurrent requests
        
    Returns:
        Dict mapping URL to content
    """
    # TODO: from concurrent.futures import ThreadPoolExecutor
    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     results = {url: content for url, content in 
    #                zip(urls, executor.map(fetch_url, urls))}
    
    # Placeholder: Sequential fetching
    results = {}
    for url in urls:
        results[url] = fetch_url(url)
    
    return results
