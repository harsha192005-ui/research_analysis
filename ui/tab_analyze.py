"""
ui/tab_analyze.py
Analyze tab — upload or pick a paper, choose a mode, run the AI pipeline.
"""
import streamlit as st
from langchain_core.messages import HumanMessage

from core.database import get_all_papers, get_paper_by_id, save_paper, save_analysis
from core.file_utils import extract_text_from_file, truncate_for_llm, title_from_filename
from core.agent import workflow, MODE_PROMPTS, ResearchState


PAPER_MODES = {"📄 Summarize Paper", "🔍 Extract Key Findings", "🔄 Full Pipeline"}

MODE_DESCRIPTIONS = {
    "📄 Summarize Paper":            ("📄", "Upload a PDF or TXT paper. Get a detailed summary + key findings + citations."),
    "🔍 Extract Key Findings":       ("🔍", "Upload a paper to extract contributions, metrics, and novel insights + research suggestions."),
    "📚 Generate Literature Review": ("📚", "Enter a research topic to generate a full structured literature review."),
    "💡 Research Suggestions":       ("💡", "Describe your research context to get a tailored guidance report + 12-month roadmap."),
    "🔄 Full Pipeline":              ("🔄", "Upload a paper to run all 5 agents — summary, findings, review, suggestions, citations."),
}

MODE_BADGES = {
    "📄 Summarize Paper":            ("badge-summarize", "SUMMARY"),
    "🔍 Extract Key Findings":       ("badge-findings",  "FINDINGS"),
    "📚 Generate Literature Review": ("badge-review",    "LIT REVIEW"),
    "💡 Research Suggestions":       ("badge-suggest",   "SUGGESTIONS"),
    "🔄 Full Pipeline":              ("badge-summarize", "FULL PIPELINE"),
}


def render(tab):
    with tab:
        # ── Mode selector ─────────────────────────────────────────────────────
        col_mode, _ = st.columns([2, 3])
        with col_mode:
            selected_mode = st.selectbox("ANALYSIS MODE", list(MODE_PROMPTS.keys()), index=0)

        icon_d, desc_d = MODE_DESCRIPTIONS[selected_mode]
        st.markdown(f"""
        <div class='mode-desc'>
            <span style='font-size:1rem;flex-shrink:0;'>{icon_d}</span>
            <span>{desc_d}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── Paper input ───────────────────────────────────────────────────────
        user_input       = ""
        extracted_filename = ""
        current_paper_id   = None

        if selected_mode in PAPER_MODES:
            st.markdown("<span class='sub-label'>Paper Source</span>", unsafe_allow_html=True)

            saved_papers   = get_all_papers()
            source_options = ["⬆ Upload new paper"]
            if saved_papers:
                source_options.append("📚 Use paper from library")

            paper_source = st.radio("source", source_options, horizontal=True, label_visibility="collapsed")

            if paper_source == "📚 Use paper from library":
                lib_map      = {f"{p['title']}  ({p['uploaded_at']})": p["id"] for p in saved_papers}
                chosen_label = st.selectbox("SELECT PAPER", list(lib_map.keys()), key="analyze_paper_pick")
                chosen_id    = lib_map[chosen_label]
                row          = get_paper_by_id(chosen_id)
                if row:
                    extracted_filename       = row["filename"]
                    extracted_text, was_trunc = truncate_for_llm(row["content"])
                    final_words              = len(extracted_text.split())
                    current_paper_id         = chosen_id

                    st.markdown(f"""
                    <div class='metric-row'>
                        <div class='metric-chip'>📄 {row["filename"]}</div>
                        <div class='metric-chip'>Words: <span>{row["word_count"]:,}</span></div>
                        <div class='metric-chip'>Sent to model: <span>{final_words:,}</span></div>
                        <div class='metric-chip teal'>✓ From library</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if was_trunc:
                        st.warning(f"⚠️ Truncated to {final_words:,} words to fit token limit.")

                    with st.expander("👁 Preview extracted text", expanded=False):
                        st.markdown(
                            f"<div class='preview-block'>{extracted_text[:3000]}"
                            f"{'...' if len(extracted_text)>3000 else ''}</div>",
                            unsafe_allow_html=True,
                        )
                    user_input = extracted_text

            else:
                uploaded_file = st.file_uploader(
                    label="upload", type=["pdf", "txt"],
                    label_visibility="collapsed",
                    help="Saved to your library automatically.",
                )
                if uploaded_file is not None:
                    with st.spinner(f"Extracting text from **{uploaded_file.name}**…"):
                        try:
                            extracted_text = extract_text_from_file(uploaded_file)
                        except RuntimeError as e:
                            st.error(str(e))
                            extracted_text = ""

                    if extracted_text.strip():
                        extracted_filename       = uploaded_file.name
                        original_words           = len(extracted_text.split())
                        extracted_text, was_trunc = truncate_for_llm(extracted_text)
                        final_words              = len(extracted_text.split())
                        title_guess              = title_from_filename(uploaded_file.name)
                        current_paper_id         = save_paper(uploaded_file.name, title_guess, extracted_text)

                        st.markdown(f"""
                        <div class='metric-row'>
                            <div class='metric-chip'>📄 {uploaded_file.name}</div>
                            <div class='metric-chip'>Original: <span>{original_words:,} words</span></div>
                            <div class='metric-chip'>Sent to model: <span>{final_words:,}</span></div>
                            <div class='metric-chip teal'>✓ Saved to library</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if was_trunc:
                            st.warning(
                                f"⚠️ Large paper ({original_words:,} words). "
                                f"Truncated to {final_words:,} words. "
                                "Abstract, Introduction and Conclusion preserved."
                            )

                        with st.expander("👁 Preview extracted text", expanded=False):
                            st.markdown(
                                f"<div class='preview-block'>{extracted_text[:3000]}"
                                f"{'...' if len(extracted_text)>3000 else ''}</div>",
                                unsafe_allow_html=True,
                            )
                        user_input = extracted_text
                    else:
                        st.warning("Could not extract text. Try a text-based PDF or .txt file.")
                else:
                    st.markdown("""
                    <div class='empty-state' style='padding:1.8rem;'>
                        <span class='empty-state-icon'>📂</span>
                        <div class='empty-state-title'>Drop your paper here</div>
                        <div class='empty-state-desc'>Supports <strong>PDF</strong> and <strong>TXT</strong> · Saved to library automatically</div>
                    </div>
                    """, unsafe_allow_html=True)

        else:
            placeholders = {
                "📚 Generate Literature Review": "Enter a research topic.\n\nExample: 'Deep Learning for Medical Image Segmentation'",
                "💡 Research Suggestions":       "Describe your research context.\n\nExample: 'I am studying federated learning for privacy-preserving healthcare AI…'",
            }
            user_input = st.text_area(
                "RESEARCH TOPIC / CONTEXT",
                placeholder=placeholders.get(selected_mode, "Enter your research topic…"),
                height=160,
            )

        # ── Run / Clear ───────────────────────────────────────────────────────
        col_run, col_clr = st.columns([1, 5])
        with col_run:
            run_clicked = st.button("▶ Analyze")
        with col_clr:
            if st.button("✕ Clear History"):
                st.session_state.history = []
                st.rerun()

        # ── Pipeline ──────────────────────────────────────────────────────────
        if run_clicked:
            if not user_input.strip():
                st.warning(
                    "Please upload a research paper (PDF or TXT) before analyzing."
                    if selected_mode in PAPER_MODES
                    else "Please enter a research topic before analyzing."
                )
            else:
                with st.spinner("Research agents working…"):
                    prompt = MODE_PROMPTS[selected_mode].format(query=user_input)
                    initial_state: ResearchState = {
                        "query":    user_input,
                        "mode":     selected_mode,
                        "messages": [HumanMessage(content=prompt)],
                        "response": "",
                    }
                    result = workflow.invoke(initial_state)
                    answer = result.get("response", "No response generated.")

                    if current_paper_id:
                        save_analysis(current_paper_id, selected_mode, answer)

                    label = extracted_filename if extracted_filename else user_input[:80]
                    st.session_state.history.append({
                        "mode":  selected_mode,
                        "input": label + ("…" if len(label) == 80 else ""),
                        "answer": answer,
                    })

                st.success("✓ Analysis complete — visit 💬 Ask Questions to query across all your papers.")

                badge_cls, badge_label = MODE_BADGES.get(selected_mode, ("badge-summarize", "RESULT"))
                st.markdown(
                    f"<div style='margin:1.2rem 0 0.4rem'><span class='mode-badge {badge_cls}'>{badge_label}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='result-card'>{answer.replace(chr(10), '<br>')}</div>",
                    unsafe_allow_html=True,
                )
                st.download_button(
                    label="⬇ Download Result",
                    data=f"Mode: {selected_mode}\n\nInput:\n{user_input}\n\n{'='*60}\n\nResult:\n{answer}",
                    file_name="research_result.txt",
                    mime="text/plain",
                )

        # ── History ───────────────────────────────────────────────────────────
        if st.session_state.history:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<span class='sub-label'>Session History</span>", unsafe_allow_html=True)
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.expander(f"{item['mode']}  ·  {item['input']}", expanded=False):
                    st.markdown(
                        f"<div class='result-card' style='margin-top:0'>{item['answer'].replace(chr(10), '<br>')}</div>",
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        label="⬇ Download",
                        data=item["answer"],
                        file_name=f"research_result_{len(st.session_state.history)-i}.txt",
                        mime="text/plain",
                        key=f"dl_{i}",
                    )