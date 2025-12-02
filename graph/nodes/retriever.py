"""
Retriever node: Performs semantic search for each subtopic.
"""

from typing import Dict, List
from graph.state import ReviewState


def retrieve_context(state: ReviewState) -> ReviewState:
    """
    For each subtopic, performs semantic retrieval from vector store.
    Retrieves top-k most relevant chunks using FAISS similarity search.
    
    Args:
        state: ReviewState with vector_store
        
    Returns:
        Updated ReviewState with retrieved_chunks per subtopic
    """
    print(f"[RETRIEVER] Retrieving context for {len(state['subtopics'])} subtopics")
    
    retrieved_chunks: Dict[str, List[Dict]] = {}
    
    # Check if vector store is available
    if not state.get("vector_store"):
        print("  Warning: No vector store available, using chunk filtering fallback")
        # Fallback: Filter chunks by subtopic
        for subtopic in state["subtopics"]:
            relevant_chunks = [
                chunk for chunk in state["chunks"]
                if chunk["metadata"]["subtopic"] == subtopic.name
            ]
            retrieved_chunks[subtopic.name] = relevant_chunks[:10]
            print(f"    {subtopic.name}: {len(relevant_chunks[:10])} chunks (filtered)")
    else:
        # Use FAISS semantic search
        vector_store = state["vector_store"]
        
        for subtopic in state["subtopics"]:
            try:
                # Perform similarity search
                query = subtopic.search_query
                results = vector_store.similarity_search(query, k=10)
                
                # Convert to chunk format
                relevant_chunks = [
                    {
                        "text": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in results
                ]
                
                retrieved_chunks[subtopic.name] = relevant_chunks
                print(f"    {subtopic.name}: {len(relevant_chunks)} chunks (semantic search)")
                
            except Exception as e:
                print(f"    Warning: Error retrieving for {subtopic.name}: {e}")
                # Fallback to filtering
                relevant_chunks = [
                    chunk for chunk in state["chunks"]
                    if chunk["metadata"]["subtopic"] == subtopic.name
                ]
                retrieved_chunks[subtopic.name] = relevant_chunks[:10]
    
    state["_retrieved_chunks"] = retrieved_chunks  # type: ignore
    
    return state
