"""
core/tools.py
LangChain tools — one per research function.
Each tool calls its dedicated LLM with a detailed prompt.
"""
from langchain.tools import tool
from core.models import summarizer_model, extractor_model, review_model, suggest_model


@tool
def paper_summarizer_tool(paper_text: str) -> str:
    """Summarize a research paper into a detailed, structured overview."""
    prompt = f"""You are a senior academic researcher and science communicator with expertise across all fields.
Your task is to produce a thorough, publication-quality summary of the research paper provided.

PAPER CONTENT:
{paper_text}

Produce a DETAILED structured summary using exactly the following sections:

---

### 1. 📌 Title, Authors & Publication Context
- Full title (if available), author names, affiliations, publication year, venue/journal.
- If not explicitly stated, infer what you can from the text.

### 2. 🎯 Research Problem & Motivation
- What specific problem or gap in knowledge does this paper address?
- Why is this problem important? What are the real-world or theoretical consequences of not solving it?
- What limitations of prior work motivated this research?

### 3. 🔬 Objectives & Research Questions
- State the primary objectives clearly.
- List the specific research questions or hypotheses being tested.

### 4. ⚙️ Methodology & Approach
- Describe the research design in detail (experimental, survey, simulation, theoretical, etc.).
- What datasets, tools, frameworks, or instruments were used?
- What is the pipeline or workflow the authors follow?
- Any novel technical contributions to methodology itself?

### 5. 📊 Results & Key Findings
- Enumerate the main results with specific numbers, metrics, or statistics where available.
- Distinguish between primary results and secondary/supporting findings.
- Were the results consistent with the hypotheses?

### 6. 💡 Contributions & Novelty
- What does this paper contribute that did not exist before?
- How does it advance the state of the art?
- Is the contribution theoretical, empirical, methodological, or applied?

### 7. 🌍 Implications & Applications
- What are the practical applications of these findings?
- Which industries, domains, or communities benefit most?
- What policy, design, or engineering decisions could be informed by this work?

### 8. ⚠️ Limitations & Threats to Validity
- What are the acknowledged or unacknowledged limitations?
- Scope constraints, dataset biases, generalizability concerns, reproducibility issues?

### 9. 🔭 Future Work
- What future directions do the authors suggest?
- What open questions remain unanswered?

---

Write each section with depth — minimum 3–5 sentences per section. Be analytical, not just descriptive.
Use precise academic language. Where numbers or metrics are available, always include them.
"""
    return summarizer_model.invoke(prompt).content


@tool
def key_findings_extractor_tool(paper_text: str) -> str:
    """Extract and deeply analyse key findings, contributions, and insights from a research paper."""
    prompt = f"""You are an expert research analyst with deep domain knowledge across science, engineering, and social sciences.
Your task is to perform a rigorous, comprehensive extraction and analysis of key findings from the paper below.

PAPER CONTENT:
{paper_text}

Produce a DETAILED extraction report using exactly the following structure:

---

### 1. 🏆 Primary Contributions (ranked by significance)
For each contribution:
- **What**: State the contribution precisely.
- **Why it matters**: Explain the scientific or practical significance.
- **How it advances prior work**: Contrast with what was known before.

### 2. 🔑 Key Findings (exhaustive bullet list)
List every significant finding. For each:
- State the finding clearly and specifically.
- Include exact numbers, percentages, p-values, accuracy scores, or effect sizes wherever present.
- Note whether the finding is expected, surprising, or contradicts existing literature.

### 3. 🧪 Technical & Methodological Innovations
- What new methods, architectures, algorithms, or frameworks are introduced?
- How do they differ from existing approaches?
- What are their computational or practical advantages?

### 4. 📈 Quantitative Results & Benchmarks
- List all reported metrics (accuracy, F1, BLEU, RMSE, etc.) with their values.
- Compare against baselines if reported.
- Note dataset sizes, experimental conditions, and reproducibility details.

### 5. 🌟 Novelty Analysis
- What is genuinely new in this work vs. incremental improvement?
- Does this paper open a new research direction or close an existing one?
- Rate novelty: Incremental / Moderate / High / Paradigm-shifting — and justify.

### 6. 🔗 Connections to Existing Literature
- Which prior works does this paper build on, challenge, or extend?
- Name specific seminal papers or authors in the field if referenced.
- Where does this fit in the broader research landscape?

### 7. 💼 Practical & Industrial Applications
- Specific use cases where these findings can be directly applied.
- Which industries or sectors would benefit most and how?
- Any deployment considerations, risks, or prerequisites?

### 8. ❓ Unresolved Questions & Research Gaps Exposed
- What questions does this paper raise but not answer?
- What gaps does it expose in the field?
- What follow-up experiments or studies are needed?

---

Be exhaustive. If data is available, always cite it. Do not omit findings even if they seem minor.
"""
    return extractor_model.invoke(prompt).content


@tool
def literature_review_tool(research_topic: str) -> str:
    """Generate a comprehensive, scholarly literature review for a given research topic."""
    prompt = f"""You are a distinguished academic with 20+ years of experience writing systematic literature reviews for top-tier journals.
Your task is to write a comprehensive, deeply analytical literature review on the topic below.

TOPIC: {research_topic}

Write a FULL scholarly literature review with the following sections.
Each section must be substantive — minimum 4–6 sentences, with depth and specificity:

---

### 1. 📖 Introduction & Scope
- Define the topic and its boundaries.
- Explain why this topic is significant in the current academic and practical landscape.
- State what this review covers and what it intentionally excludes.
- Mention the time period and types of sources considered.

### 2. 🏛️ Theoretical Foundations & Conceptual Framework
- What are the foundational theories, models, or frameworks underpinning this field?
- Who are the key theorists and what did they establish?
- Define essential terminology and constructs used across the literature.
- How have theoretical perspectives shifted over time?

### 3. 📅 Historical Evolution & Milestones
- Trace the development of this field chronologically.
- Identify landmark papers, discoveries, or technological breakthroughs.
- What triggered major paradigm shifts in this area?
- How has the field matured from early work to current state?

### 4. 🔥 Major Research Themes & Active Debates
- Identify 4–6 dominant research themes currently active in this area.
- For each theme: describe the core question, leading approaches, and key findings.
- Where do researchers disagree? What are the active controversies or competing schools of thought?

### 5. ⚙️ Methodological Landscape
- What research methodologies dominate this field?
- What datasets, benchmarks, or experimental setups are most commonly used?
- What are the methodological strengths and weaknesses prevalent in this literature?
- Are there emerging methodological trends?

### 6. 📊 Key Empirical Findings Across the Literature
- Synthesise what the collective body of research has established as fact.
- Where is there strong consensus? Where is evidence mixed or contradictory?
- Highlight meta-analyses or systematic reviews that aggregate findings.

### 7. 🚧 Gaps, Limitations & Underexplored Areas
- What questions remain unanswered despite significant research effort?
- Which populations, contexts, or scenarios are understudied?
- What methodological weaknesses pervade the existing literature?
- Where is there a lack of replication or longitudinal data?

### 8. 🌐 Interdisciplinary Connections
- What other fields intersect with or inform this topic?
- What can this field learn from adjacent disciplines?
- Are there productive cross-disciplinary collaborations worth highlighting?

### 9. 🔭 Future Research Directions
- What are the most promising and needed research directions?
- Propose 4–5 specific, concrete research questions the field should prioritise.

### 10. ✅ Synthesis & Conclusion
- Summarise the state of the field in 2–3 paragraphs.
- What is the overall trajectory of this research area?
- What is the most important takeaway for a new researcher entering this field?

---

Write in formal academic prose throughout. Be specific — name influential research clusters where known,
and use precise language. Avoid vague generalities.
"""
    return review_model.invoke(prompt).content


@tool
def research_suggestion_tool(context: str) -> str:
    """Provide deep, context-aware research suggestions and a concrete 12-month roadmap."""
    prompt = f"""You are a world-class research mentor and academic strategist who has guided hundreds of PhD students and faculty.
Your task is to provide deeply personalised, actionable, and strategic research guidance based on the context below.

RESEARCH CONTEXT:
{context}

Produce a COMPREHENSIVE research guidance report:

---

### 1. 🗺️ Research Landscape Overview
- Where does this research sit within the broader academic landscape?
- What is the current state of knowledge in this area?
- Is this a mature field, an emerging area, or a niche domain?

### 2. 🔬 Specific Research Questions Worth Pursuing (minimum 6)
For each question:
- State the question precisely.
- Explain why it is important and what gap it fills.
- Suggest a feasible methodological approach.
- Estimate difficulty: Accessible / Moderate / Challenging.

### 3. 📚 Related Research Areas to Explore (minimum 6)
For each area:
- Name the area and explain its relevance.
- Identify 2–3 key papers or researchers associated with it.
- Describe how engaging with this area would strengthen the research.

### 4. ⚙️ Methodological Recommendations
- What research designs are best suited to this topic?
- What datasets, tools, or experimental setups should be considered?
- What statistical or analytical methods are most appropriate?
- What methodological pitfalls should be avoided?

### 5. 📰 Key Journals, Conferences & Publication Venues
- List 5–8 top venues where this research is published.
- For each: focus area, impact level, and submission considerations.

### 6. 🤝 Collaboration & Interdisciplinary Opportunities
- Which adjacent fields should this researcher engage with?
- What types of collaborators would strengthen the work?
- Are there specific research groups or labs known for this area?

### 7. 🛠️ Tools, Resources & Infrastructure
- What software, frameworks, or platforms are essential?
- What datasets or corpora should the researcher familiarise themselves with?

### 8. ⚠️ Challenges & Risk Mitigation
- What are the main risks or obstacles in this direction?
- What common mistakes do researchers in this area make?
- How can the researcher de-risk their work early?

### 9. 🗓️ Concrete Research Roadmap (12-month plan)
- **Months 1–2**: Foundation — literature, tools, preliminary experiments
- **Months 3–4**: Problem formulation and pilot study
- **Months 5–7**: Core experimental work
- **Months 8–9**: Analysis and writing
- **Months 10–12**: Submission, revision, and dissemination
- For each phase: specific deliverables and milestones.

### 10. 💎 Strategic Advice
- What would distinguish excellent from average work in this area?
- What is the single most impactful thing this researcher could do in the next 30 days?
- What long-term habits will make them successful in this direction?

---

Be specific, practical, and encouraging. Every suggestion should be directly relevant to the context provided.
"""
    return suggest_model.invoke(prompt).content


@tool
def citation_formatter_tool(paper_info: str) -> str:
    """Extract paper metadata and format into all major citation styles with BibTeX."""
    prompt = f"""You are an expert academic librarian and citation specialist with mastery of all major citation styles.
Your task is to extract all available bibliographic information from the text and produce properly formatted citations.

PAPER CONTENT / INFO:
{paper_info}

---

### 📋 Extracted Bibliographic Information
First, extract and list all available metadata:
- **Title**: (extract from text)
- **Authors**: (list all authors found)
- **Year**: (publication year)
- **Journal/Conference/Publisher**:
- **Volume / Issue / Pages**: (if available)
- **DOI / URL**: (if available)
- **Institution/Affiliation**: (if mentioned)

Note: Mark any field as [Not found in text] if unavailable.

---

### 📎 Formatted Citations

**APA 7th Edition:**
[Full APA citation here]

**MLA 9th Edition:**
[Full MLA citation here]

**Chicago Author-Date:**
[Full Chicago citation here]

**IEEE:**
[Full IEEE citation here]

**Harvard:**
[Full Harvard citation here]

**Vancouver (Medical/Biomedical):**
[Full Vancouver citation here]

---

### 📝 In-text Citation Examples
**APA**: (Author, Year)  |  **MLA**: (Author Page)  |  **Chicago**: (Author Year, Page)  |  **IEEE**: [N]

---

### 💡 BibTeX Entry
```bibtex
@article{{key,
  title   = {{}},
  author  = {{}},
  year    = {{}},
  journal = {{}},
  volume  = {{}},
  pages   = {{}}
}}
```

If critical information is missing, provide [Unknown] placeholders and note what is needed to complete the citation.
"""
    return extractor_model.invoke(prompt).content


# Exported list for LangGraph
ALL_TOOLS = [
    paper_summarizer_tool,
    key_findings_extractor_tool,
    literature_review_tool,
    research_suggestion_tool,
    citation_formatter_tool,
]