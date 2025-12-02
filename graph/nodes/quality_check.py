"""
Quality check node for conditional edges.

This node evaluates the quality of search and fetch results,
determining whether to proceed or retry with different queries.
"""

from typing import Dict
from graph.state import ReviewState


def check_quality(state: ReviewState) -> ReviewState:
    """
    Checks the quality of collected documents and decides next action.
    
    Evaluates:
    - Number of documents fetched
    - Number of valid URLs found
    - Completeness across subtopics
    
    Args:
        state: Current ReviewState
        
    Returns:
        Updated state with quality_check_passed flag
    """
    print("[QUALITY CHECK] Evaluating search and fetch results")
    
    num_documents = len(state["documents"])
    num_subtopics = len(state["subtopics"])
    
    # Calculate metrics
    docs_per_subtopic = num_documents / max(num_subtopics, 1)
    
    print(f"  Documents fetched: {num_documents}")
    print(f"  Subtopics planned: {num_subtopics}")
    print(f"  Average docs per subtopic: {docs_per_subtopic:.1f}")
    
    # Quality thresholds
    MIN_TOTAL_DOCS = 5
    MIN_DOCS_PER_SUBTOPIC = 0.5
    
    # Determine if quality is sufficient
    quality_passed = (
        num_documents >= MIN_TOTAL_DOCS and
        docs_per_subtopic >= MIN_DOCS_PER_SUBTOPIC
    )
    
    if quality_passed:
        print("  Quality check: PASSED - Proceeding to RAG pipeline")
    else:
        print("  Quality check: WARNING - Low document count, but proceeding")
        print("    Recommendation: Results may be limited")
    
    # Store quality flag in state (for conditional routing)
    state["_quality_passed"] = quality_passed  # type: ignore
    
    return state


def should_retry_search(state: ReviewState) -> str:
    """
    Conditional edge function to decide whether to retry search or continue.
    
    Args:
        state: Current ReviewState
        
    Returns:
        "retry" or "continue"
    """
    quality_passed = state.get("_quality_passed", True)
    retry_count = state.get("_retry_count", 0)
    
    MAX_RETRIES = 1  # Allow one retry
    
    if not quality_passed and retry_count < MAX_RETRIES:
        print(f"[CONDITIONAL] Retrying search (attempt {retry_count + 1}/{MAX_RETRIES})")
        return "retry"
    else:
        print("[CONDITIONAL] Continuing to RAG pipeline")
        return "continue"
