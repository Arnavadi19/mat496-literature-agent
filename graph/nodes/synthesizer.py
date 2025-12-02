"""
Synthesizer node: Creates final comprehensive literature review.
"""

import os
from pathlib import Path
from graph.state import ReviewState
from langchain_openai import ChatOpenAI


def synthesize_review(state: ReviewState) -> ReviewState:
    """
    Synthesizes all subtopic summaries into a comprehensive literature review.
    
    Structure:
    - Introduction
    - Key Themes (organized by subtopic summaries)
    - Research Gaps
    - Conclusion
    
    Args:
        state: ReviewState with summaries
        
    Returns:
        Updated ReviewState with final_review
    """
    print("[SYNTHESIZER] Synthesizing final literature review")
    
    # Load prompt template
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "synthesizer_prompt.txt"
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()
    
    # Format all summaries for the prompt
    summaries_text = ""
    for i, summary in enumerate(state["summaries"], 1):
        summaries_text += f"\n## Subtopic {i}: {summary.subtopic}\n\n"
        summaries_text += f"**Summary:** {summary.summary}\n\n"
        summaries_text += "**Key Findings:**\n"
        for finding in summary.key_findings:
            summaries_text += f"- {finding}\n"
        summaries_text += f"\n**Sources:** {', '.join(summary.sources[:3])}\n"
    
    # Format prompt
    prompt = prompt_template.format(
        topic=state['topic'],
        summaries=summaries_text
    )
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        print("  Calling OpenAI for final synthesis...")
        
        # Invoke LLM for final review
        response = llm.invoke(prompt)
        final_review = response.content
        
        print("  Final review synthesized")
        
    except Exception as e:
        print(f"  Warning: Error calling OpenAI: {e}")
        print("  Using placeholder review")
        
        # Fallback to placeholder
        final_review = _create_placeholder_review(state)
    
    state["final_review"] = final_review
    return state


def _create_placeholder_review(state: ReviewState) -> str:
    """Creates a placeholder review when LLM call fails."""
    final_review = f"""# Literature Review: {state['topic']}

## Introduction
This literature review synthesizes research on {state['topic']}.

## Key Themes

"""
    
    for summary in state["summaries"]:
        final_review += f"### {summary.subtopic}\n\n"
        final_review += f"{summary.summary}\n\n"
        final_review += "**Key Findings:**\n"
        for finding in summary.key_findings:
            final_review += f"- {finding}\n"
        final_review += "\n"
    
    final_review += """
## Research Gaps
[Placeholder: OpenAI integration needed to identify gaps]

## Conclusion
[Placeholder: OpenAI integration needed for synthesis]
"""
    
    return final_review
