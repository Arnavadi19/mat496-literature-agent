"""
Main entry point for the Autonomous Literature Review Agent.

This script demonstrates LangGraph concepts:
- State management with TypedDict
- Node definitions (functions that transform state)
- Graph construction with nodes and edges
- Graph compilation and execution
"""

import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langgraph.graph import StateGraph, END
from graph.state import ReviewState
from graph.nodes.planner import plan_subtopics
from graph.nodes.searcher import search_web
from graph.nodes.fetcher import fetch_pages
from graph.nodes.quality_check import check_quality, should_retry_search
from graph.nodes.chunk_embed import chunk_and_embed
from graph.nodes.retriever import retrieve_context
from graph.nodes.summarizer import summarize_subtopics
from graph.nodes.synthesizer import synthesize_review


def build_graph() -> StateGraph:
    """
    Constructs the LangGraph workflow with conditional edges.
    
    Graph flow:
    1. Planner → Generates subtopics
    2. Searcher → Searches web for URLs
    3. Fetcher → Fetches webpage content
    4. Quality Check → Evaluates results
       - If quality low and retries available: retry searcher
       - Otherwise: continue to RAG pipeline
    5. Chunk & Embed → Creates vector store
    6. Retriever → Semantic retrieval
    7. Summarizer → Per-subtopic summaries
    8. Synthesizer → Final literature review -> END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize the graph with ReviewState
    workflow = StateGraph(ReviewState)
    
    # Add nodes (each is a function that takes state and returns updated state)
    workflow.add_node("planner", plan_subtopics)
    workflow.add_node("searcher", search_web)
    workflow.add_node("fetcher", fetch_pages)
    workflow.add_node("quality_check", check_quality)
    workflow.add_node("chunk_embed", chunk_and_embed)
    workflow.add_node("retriever", retrieve_context)
    workflow.add_node("summarizer", summarize_subtopics)
    workflow.add_node("synthesizer", synthesize_review)
    
    # Define edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "fetcher")
    workflow.add_edge("fetcher", "quality_check")
    
    # Conditional edge: retry search or continue to RAG
    workflow.add_conditional_edges(
        "quality_check",
        should_retry_search,
        {
            "retry": "searcher",  # Go back to searcher
            "continue": "chunk_embed"  # Continue to RAG pipeline
        }
    )
    
    workflow.add_edge("chunk_embed", "retriever")
    workflow.add_edge("retriever", "summarizer")
    workflow.add_edge("summarizer", "synthesizer")
    workflow.add_edge("synthesizer", END)
    
    # Compile the graph
    return workflow.compile()


def run_literature_review(topic: str) -> Dict:
    """
    Executes the literature review workflow for a given topic.
    
    Args:
        topic: Research topic to review
        
    Returns:
        Final state with completed literature review
    """
    print(f"\n{'='*60}")
    print(f"Starting Literature Review for: {topic}")
    print(f"{'='*60}\n")
    
    # Create initial state
    initial_state: ReviewState = {
        "topic": topic,
        "subtopics": [],
        "documents": [],
        "chunks": [],
        "summaries": [],
        "final_review": None,
        "vector_store": None,
        "_search_results": None,
        "_retrieved_chunks": None,
        "_quality_passed": None,
        "_retry_count": 0,
    }
    
    # Create and run the graph
    graph = create_review_graph()
    final_state = graph.invoke(initial_state)
    
    return final_state


def main():
    """
    Main function to demonstrate the literature review agent.
    
    TODO: Add command-line argument parsing
    TODO: Add output file options (markdown, PDF)
    TODO: Add configuration file support
    """
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found!")
        print("\nPlease create a .env file with your API key:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key to .env")
        print("\nExample .env file:")
        print("   OPENAI_API_KEY=sk-your-key-here")
        print("   OPENAI_MODEL=gpt-4")
        return
    
    print("OpenAI API key loaded from .env file\n")
    
    # Example topic
    topic = "Transformer architectures in natural language processing"
    
    # TODO: Uncomment when API keys are configured
    # import os
    # if not os.getenv("OPENAI_API_KEY"):
    #     print("Error: OPENAI_API_KEY not set")
    #     return
    
    # Run the review
    final_state = run_literature_review(topic)
    
    # Display results
    print(f"\n{'='*60}")
    print("LITERATURE REVIEW COMPLETE")
    print(f"{'='*60}\n")
    
    print(f"Subtopics Generated: {len(final_state['subtopics'])}")
    print(f"Documents Fetched: {len(final_state['documents'])}")
    print(f"Summaries Created: {len(final_state['summaries'])}")
    
    print(f"\n{'='*60}")
    print("FINAL REVIEW")
    print(f"{'='*60}\n")
    print(final_state["final_review"])
    
    # TODO: Save to file
    # output_file = f"review_{topic.replace(' ', '_')}.md"
    # with open(output_file, 'w') as f:
    #     f.write(final_state["final_review"])
    # print(f"\nReview saved to: {output_file}")


if __name__ == "__main__":
    main()
