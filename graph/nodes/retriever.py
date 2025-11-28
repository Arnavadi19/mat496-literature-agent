"""
Retriever node: Performs semantic search for each subtopic.
"""

from typing import Dict, List
from graph.state import ReviewState


def retrieve_context(state: ReviewState) -> ReviewState:
    """
    For each subtopic, performs semantic retrieval from vector store.
    Retrieves top-k most relevant chunks.
    
    TODO: Query vector store with subtopic query
    TODO: Retrieve top 5-10 most relevant chunks per subtopic
    TODO: Store retrieved chunks organized by subtopic
    
    Args:
        state: ReviewState with vector_store
        
    Returns:
        Updated ReviewState with retrieved_chunks per subtopic
    """
    print(f"[RETRIEVER] Retrieving context for {len(state['subtopics'])} subtopics")
    
    # TODO: For each subtopic:
    #   - Use subtopic.search_query to query vector store
    #   - vector_store.similarity_search(query, k=10)
    #   - Organize results by subtopic
    
    # Placeholder: Store retrieval results
    retrieved_chunks: Dict[str, List[Dict]] = {}
    
    for subtopic in state["subtopics"]:
        # In real implementation, query FAISS
        # results = state["vector_store"].similarity_search(subtopic.search_query, k=10)
        
        # Placeholder: Filter chunks by subtopic
        relevant_chunks = [
            chunk for chunk in state["chunks"]
            if chunk["metadata"]["subtopic"] == subtopic.name
        ]
        retrieved_chunks[subtopic.name] = relevant_chunks[:5]
    
    state["_retrieved_chunks"] = retrieved_chunks  # type: ignore
    
    return state
