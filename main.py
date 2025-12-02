"""
Main entry point for the Autonomous Literature Review Agent.

This script demonstrates LangGraph concepts:
- State management with TypedDict
- Node definitions (functions that transform state)
- Graph construction with nodes and edges
- Graph compilation and execution
"""

import os
import argparse
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


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments with topic and output file
    """
    parser = argparse.ArgumentParser(
        description="Autonomous Literature Review Agent - Generate comprehensive literature reviews using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Machine learning in healthcare"
  python main.py --topic "Climate change impacts" --output review.md
  python main.py  # Uses default topic
        """
    )
    
    parser.add_argument(
        "--topic",
        "-t",
        type=str,
        default="Transformer architectures in natural language processing",
        help="Research topic for literature review (default: Transformer architectures in NLP)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file to save the literature review (default: print to console)"
    )
    
    return parser.parse_args()



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


def main():
    """
    Main function to run the literature review agent.
    
    Parses command-line arguments, validates configuration,
    and executes the literature review workflow.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
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
    
    # Use topic from command-line arguments
    topic = args.topic
    
    print("\n" + "="*60)
    print(f"Starting Literature Review for: {topic}")
    print("="*60 + "\n")
    
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
    graph = build_graph()
    result = graph.invoke(initial_state)
    
    # Display results
    print("\n" + "="*60)
    print("LITERATURE REVIEW COMPLETE")
    print("="*60 + "\n")
    
    print(f"Subtopics Generated: {len(result['subtopics'])}")
    print(f"Documents Fetched: {len(result['documents'])}")
    print(f"Summaries Created: {len(result['summaries'])}")
    
    print("\n" + "="*60)
    print("FINAL REVIEW")
    print("="*60 + "\n")
    
    final_review = result.get("final_review", "No review generated")
    print(final_review)
    
    # Save to file if output path specified
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Literature Review: {topic}\n\n")
            f.write(f"**Generated by**: Autonomous Literature Review Agent\n\n")
            f.write(f"**Subtopics Analyzed**: {len(result['subtopics'])}\n\n")
            f.write(f"**Documents Reviewed**: {len(result['documents'])}\n\n")
            f.write("---\n\n")
            f.write(final_review)
        
        print(f"\n\nLiterature review saved to: {output_path.absolute()}")


if __name__ == "__main__":
    main()
