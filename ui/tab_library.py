"""
ui/tab_library.py
Paper Library tab — browse, inspect, and delete stored papers and their analyses.
"""
import streamlit as st
from core.database import get_all_papers, get_analyses_for_paper, delete_paper


def render(tab):
    with tab:
        lib_papers = get_all_papers()

        if not lib_papers:
            st.markdown("""
            <div class='empty-state'>
                <span class='empty-state-icon'>📭</span>
                <div class='empty-state-title'>Your library is empty</div>
                <div class='empty-state-desc'>
                    Upload a paper in <strong>🔬 Analyze</strong> to get started.<br>
                    All uploaded papers are stored here and automatically used in Q&amp;A.
                </div>
            </div>
            """, unsafe_allow_html=True)
            return

        # ── Summary row ───────────────────────────────────────────────────────
        total_w = sum(p["word_count"] for p in lib_papers)
        st.markdown(f"""
        <div class='metric-row' style='margin-bottom:1.2rem;'>
            <div class='metric-chip teal'>📚 {len(lib_papers)} papers</div>
            <div class='metric-chip'>Total words: <span>{total_w:,}</span></div>
            <div class='metric-chip'>All used automatically in Q&amp;A ✓</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Paper cards ───────────────────────────────────────────────────────
        for paper in lib_papers:
            analyses  = get_analyses_for_paper(paper["id"])
            ana_count = len(analyses)

            with st.expander(f"📄  {paper['title']}", expanded=False):
                # Metadata card
                st.markdown(f"""
                <div class='paper-card' style='margin-bottom:0.8rem;'>
                    <div class='paper-card-title'>{paper["title"]}</div>
                    <div class='paper-card-meta'>
                        <span>📁 {paper["filename"]}</span>
                        <span>📝 {paper["word_count"]:,} words</span>
                        <span>🕐 {paper["uploaded_at"]}</span>
                        <span>🔍 {ana_count} analysis saved</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🗑 Delete paper", key=f"libdel_{paper['id']}"):
                    delete_paper(paper["id"])
                    st.rerun()

                # Saved analyses (flat cards — no nested expanders)
                if analyses:
                    st.markdown(
                        f"<span class='sub-label' style='margin-top:0.8rem;display:block;'>"
                        f"Saved analyses ({ana_count})</span>",
                        unsafe_allow_html=True,
                    )
                    for ana in analyses:
                        st.markdown(f"""
                        <div style='background:var(--bg3);border:1px solid var(--border);
                                    border-radius:var(--radius-sm);padding:0.7rem 1rem;margin-bottom:0.5rem;'>
                            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;'>
                                <span class='mode-badge badge-summarize'>{ana["mode"]}</span>
                                <span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:var(--muted);'>
                                    {ana["created_at"]}
                                </span>
                            </div>
                            <div style='font-size:0.85rem;line-height:1.7;color:var(--text2);
                                        max-height:180px;overflow-y:auto;'>
                                {ana["result"][:800].replace(chr(10), "<br>")}
                                {"…" if len(ana["result"]) > 800 else ""}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.download_button(
                            "⬇ Download full analysis",
                            data=ana["result"],
                            file_name=f"analysis_{paper['id']}_{ana['created_at'][:10]}.txt",
                            mime="text/plain",
                            key=f"ana_dl_{paper['id']}_{ana['created_at']}",
                        )