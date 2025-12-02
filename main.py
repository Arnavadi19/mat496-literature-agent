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
from graph.nodes.chunk_embed import chunk_and_embed
from graph.nodes.retriever import retrieve_context
from graph.nodes.summarizer import summarize_subtopics
from graph.nodes.synthesizer import synthesize_review


def create_review_graph() -> StateGraph:
    """
    Constructs the LangGraph for the literature review workflow.
    
    Graph structure:
        START -> plan_subtopics -> search_web -> fetch_pages 
        -> chunk_embed -> retrieve_context -> summarize_subtopics 
        -> synthesize_review -> END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize the graph with ReviewState
    workflow = StateGraph(ReviewState)
    
    # Add nodes (each is a function that takes state and returns updated state)
    workflow.add_node("plan_subtopics", plan_subtopics)
    workflow.add_node("search_web", search_web)
    workflow.add_node("fetch_pages", fetch_pages)
    workflow.add_node("chunk_embed", chunk_and_embed)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("summarize_subtopics", summarize_subtopics)
    workflow.add_node("synthesize_review", synthesize_review)
    
    # Define edges (workflow flow)
    workflow.set_entry_point("plan_subtopics")
    workflow.add_edge("plan_subtopics", "search_web")
    workflow.add_edge("search_web", "fetch_pages")
    workflow.add_edge("fetch_pages", "chunk_embed")
    workflow.add_edge("chunk_embed", "retrieve_context")
    workflow.add_edge("retrieve_context", "summarize_subtopics")
    workflow.add_edge("summarize_subtopics", "synthesize_review")
    workflow.add_edge("synthesize_review", END)
    
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
        print("❌ Error: OPENAI_API_KEY not found!")
        print("\n📝 Please create a .env file with your API key:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key to .env")
        print("\nExample .env file:")
        print("   OPENAI_API_KEY=sk-your-key-here")
        print("   OPENAI_MODEL=gpt-4")
        return
    
    print("✅ OpenAI API key loaded from .env file\n")
    
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
