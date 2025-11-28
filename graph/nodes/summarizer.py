"""
Summarizer node: Creates academic summaries for each subtopic.
"""

from typing import List
from graph.state import ReviewState, Summary


def summarize_subtopics(state: ReviewState) -> ReviewState:
    """
    For each subtopic, uses LLM to summarize retrieved chunks into
    clean academic summaries.
    
    TODO: Load prompt from prompts/summarizer_prompt.txt
    TODO: For each subtopic, create prompt with retrieved chunks
    TODO: Call LLM to generate structured summary
    TODO: Use Pydantic model for structured output
    
    Args:
        state: ReviewState with retrieved chunks
        
    Returns:
        Updated ReviewState with summaries
    """
    print(f"[SUMMARIZER] Summarizing {len(state['subtopics'])} subtopics")
    
    # TODO: from langchain_openai import ChatOpenAI
    # TODO: Load summarizer_prompt.txt
    # TODO: For each subtopic:
    #   - Gather retrieved chunks
    #   - Format prompt with chunks
    #   - Call LLM with structured output (Summary model)
    #   - Collect all summaries
    
    retrieved_chunks = state.get("_retrieved_chunks", {})
    summaries: List[Summary] = []
    
    for subtopic in state["subtopics"]:
        chunks = retrieved_chunks.get(subtopic.name, [])
        
        # Placeholder: Create mock summary
        summaries.append(
            Summary(
                subtopic=subtopic.name,
                summary=f"Academic summary for {subtopic.name}. "
                        f"Based on {len(chunks)} retrieved sources.",
                key_findings=[
                    "Finding 1: Placeholder finding",
                    "Finding 2: Another finding",
                ],
                sources=[chunk["metadata"]["url"] for chunk in chunks[:3]]
            )
        )
    
    state["summaries"] = summaries
    return state
