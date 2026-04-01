"""
core/agent.py
LangGraph workflow — ResearchState + deterministic agent node + compiled graph.
"""
from typing import TypedDict, Annotated
from operator import add

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from core.tools import (
    paper_summarizer_tool,
    key_findings_extractor_tool,
    literature_review_tool,
    research_suggestion_tool,
    citation_formatter_tool,
)


# ── State ─────────────────────────────────────────────────────────────────────

class ResearchState(TypedDict):
    query: str
    mode: str
    messages: Annotated[list, add]
    response: str


# ── Mode prompt templates (used by app to build the initial HumanMessage) ────

MODE_PROMPTS: dict[str, str] = {
    "📄 Summarize Paper": """
You are an AI research assistant. Summarize this paper comprehensively.
Input: {query}
""",
    "🔍 Extract Key Findings": """
You are an AI research analyst. Extract all key findings from this paper.
Input: {query}
""",
    "📚 Generate Literature Review": """
You are an AI academic writing assistant. Generate a full literature review.
Topic: {query}
""",
    "💡 Research Suggestions": """
You are an AI research advisor. Provide detailed research guidance.
Context: {query}
""",
    "🔄 Full Pipeline": """
You are a comprehensive AI research assistant. Run the full analysis pipeline.
Input: {query}
""",
}


# ── Agent node — deterministic direct tool calls ──────────────────────────────

def research_agent_node(state: ResearchState) -> ResearchState:
    """
    Call tools directly without relying on LLM function-calling routing,
    which avoids tool_use_failed errors on weaker models.
    """
    query = state["query"]
    mode  = state["mode"]
    parts: list[str] = []

    if mode == "📄 Summarize Paper":
        parts.append("## 📄 Detailed Summary\n"
                     + paper_summarizer_tool.invoke({"paper_text": query}))
        parts.append("## 🔍 Key Findings\n"
                     + key_findings_extractor_tool.invoke({"paper_text": query}))
        parts.append("## 📖 Citations\n"
                     + citation_formatter_tool.invoke({"paper_info": query}))

    elif mode == "🔍 Extract Key Findings":
        parts.append("## 🔍 Key Findings & Contributions\n"
                     + key_findings_extractor_tool.invoke({"paper_text": query}))
        parts.append("## 💡 Related Research Suggestions\n"
                     + research_suggestion_tool.invoke({"context": query}))

    elif mode == "📚 Generate Literature Review":
        parts.append("## 📚 Literature Review\n"
                     + literature_review_tool.invoke({"research_topic": query}))
        parts.append("## 💡 Research Gaps & Next Steps\n"
                     + research_suggestion_tool.invoke({"context": query}))

    elif mode == "💡 Research Suggestions":
        parts.append("## 💡 Research Guidance & Roadmap\n"
                     + research_suggestion_tool.invoke({"context": query}))
        parts.append("## 📚 Theoretical Background\n"
                     + literature_review_tool.invoke({"research_topic": query}))

    elif mode == "🔄 Full Pipeline":
        parts.append("## 📄 Summary\n"
                     + paper_summarizer_tool.invoke({"paper_text": query}))
        parts.append("## 🔍 Key Findings\n"
                     + key_findings_extractor_tool.invoke({"paper_text": query}))
        parts.append("## 📚 Literature Review\n"
                     + literature_review_tool.invoke({"research_topic": query}))
        parts.append("## 💡 Research Suggestions\n"
                     + research_suggestion_tool.invoke({"context": query}))
        parts.append("## 📖 Citations\n"
                     + citation_formatter_tool.invoke({"paper_info": query}))
    else:
        parts.append(query)

    text = "\n\n---\n\n".join(parts)
    return {
        **state,
        "response": text,
        "messages": state["messages"] + [AIMessage(content=text)],
    }


# ── Graph ─────────────────────────────────────────────────────────────────────

def build_workflow():
    graph = StateGraph(ResearchState)
    graph.add_node("research_agent", research_agent_node)
    graph.add_edge(START, "research_agent")
    graph.add_edge("research_agent", END)
    return graph.compile()


workflow = build_workflow()