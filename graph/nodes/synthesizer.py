"""
Synthesizer node: Creates final comprehensive literature review.
"""

from graph.state import ReviewState


def synthesize_review(state: ReviewState) -> ReviewState:
    """
    Synthesizes all subtopic summaries into a comprehensive literature review.
    
    Structure:
    - Introduction
    - Key Themes (organized by subtopic summaries)
    - Research Gaps
    - Conclusion
    
    TODO: Load prompt from prompts/synthesizer_prompt.txt
    TODO: Format all summaries into prompt
    TODO: Call LLM to generate final review
    TODO: Store in state["final_review"]
    
    Args:
        state: ReviewState with summaries
        
    Returns:
        Updated ReviewState with final_review
    """
    print("[SYNTHESIZER] Synthesizing final literature review")
    
    # TODO: from langchain_openai import ChatOpenAI
    # TODO: Load synthesizer_prompt.txt
    # TODO: Format prompt with topic, all summaries
    # TODO: Call LLM for final synthesis
    
    # Placeholder implementation
    final_review = f"""
# Literature Review: {state['topic']}

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
[TODO: LLM will identify gaps across summaries]

## Conclusion
[TODO: LLM will synthesize conclusions]
"""
    
    state["final_review"] = final_review
    return state
