"""
app.py  ←  Entry point
Run with:  streamlit run app.py
"""
import streamlit as st

from core.database import init_db, get_all_papers
from assets.styles import CSS
import ui.tab_qa       as tab_qa
import ui.tab_analyze  as tab_analyze
import ui.tab_library  as tab_library
from dotenv import load_dotenv
load_dotenv()

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

# ── DB init ───────────────────────────────────────────────────────────────────
init_db()

# ── Session state ─────────────────────────────────────────────────────────────
if "history"     not in st.session_state: st.session_state.history     = []
if "qa_messages" not in st.session_state: st.session_state.qa_messages = []
if "qa_pending"  not in st.session_state: st.session_state.qa_pending  = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.6rem 0 1rem;'>
        <div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;'>
            <div style='width:32px;height:32px;background:var(--gold-dim);border:1px solid var(--gold-border);
                        border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;'>🔬</div>
            <div>
                <p style='font-family:DM Serif Display,serif;font-size:1rem;color:var(--text);margin:0;'>
                    Research Assistant</p>
                <p style='font-size:0.7rem;color:var(--muted);margin:0;'>LangGraph · Groq · SQLite</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live stats
    all_papers  = get_all_papers()
    total_words = sum(p["word_count"] for p in all_papers)
    st.markdown(f"""
    <div class='sb-stat'>
        <span class='sb-stat-label'>📚 Papers saved</span>
        <span class='sb-stat-value'>{len(all_papers)}</span>
    </div>
    <div class='sb-stat'>
        <span class='sb-stat-label'>🔍 Total words</span>
        <span class='sb-stat-value'>{total_words:,}</span>
    </div>
    <div class='sb-stat'>
        <span class='sb-stat-label'>⚡ Session analyses</span>
        <span class='sb-stat-value'>{len(st.session_state.history)}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<span class='sub-label'>AI Agents</span>", unsafe_allow_html=True)

    for icon, name, desc in [
        ("📄", "Paper Summarizer",    "Structured abstracts & overviews"),
        ("🔍", "Findings Extractor",  "Key results & contributions"),
        ("📚", "Literature Reviewer", "Full academic literature survey"),
        ("💡", "Research Advisor",    "Questions, gaps & next steps"),
        ("📖", "Citation Formatter",  "APA · MLA · Chicago · IEEE · BibTeX"),
    ]:
        st.markdown(f"""
        <div class='agent-card'>
            <div class='agent-card-icon'>{icon}</div>
            <div>
                <div class='agent-card-name'>{name}</div>
                <div class='agent-card-desc'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem;color:var(--muted);line-height:1.8;'>
        <b style='color:var(--text2);'>💬 Ask Questions</b> — query all papers at once<br>
        <b style='color:var(--text2);'>🔬 Analyze</b> — run AI agents on a paper<br>
        <b style='color:var(--text2);'>🗄 Library</b> — manage your paper collection
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='app-header'>
    <div class='app-header-icon'>🔬</div>
    <div>
        <h1>Research Assistant</h1>
        <p>AI-powered · Summarize · Extract · Ask questions across your paper library</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
t_qa, t_analyze, t_library = st.tabs(["💬 Ask Questions", "🔬 Analyze", "🗄 Library"])

tab_qa.render(t_qa)
tab_analyze.render(t_analyze)
tab_library.render(t_library)