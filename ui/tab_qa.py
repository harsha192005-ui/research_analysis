"""
ui/tab_qa.py
Ask Questions tab — multi-turn chat grounded in the full paper library.
"""
import datetime
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from core.database import get_all_papers, get_paper_by_id
from core.models import suggest_model


def render(tab):
    with tab:
        qa_all_papers = get_all_papers()

        # ── Library status banner ─────────────────────────────────────────────
        if qa_all_papers:
            titles   = "  ·  ".join(p["title"] for p in qa_all_papers[:3])
            overflow = f"  +{len(qa_all_papers)-3} more" if len(qa_all_papers) > 3 else ""
            st.markdown(f"""
            <div class='banner banner-teal'>
                📚 <strong>{len(qa_all_papers)} paper(s)</strong> in library &nbsp;·&nbsp; {titles}{overflow}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='banner banner-gold'>
                💡 No papers yet — upload one in <strong>🔬 Analyze</strong> to enable context-aware Q&amp;A.
            </div>
            """, unsafe_allow_html=True)

        # ── Chat history ──────────────────────────────────────────────────────
        if st.session_state.qa_messages:
            for msg in st.session_state.qa_messages:
                ts = msg.get("ts", "")
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class='chat-wrap'>
                      <div class='chat-user'>
                        <div class='chat-user-inner'>
                          <div class='chat-user-bubble'>{msg["content"]}</div>
                          <div class='chat-ts'>{ts}</div>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='chat-wrap'>
                      <div class='chat-bot'>
                        <div class='chat-bot-avatar'>🔬</div>
                        <div class='chat-bot-inner'>
                          <div class='chat-bot-bubble'>{msg["content"].replace(chr(10), "<br>")}</div>
                          <div class='chat-ts'>{ts}</div>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
            c1, c2, _ = st.columns([2, 2, 8])
            with c1:
                st.download_button(
                    "⬇ Export chat",
                    data="\n\n".join(
                        f"{'You' if m['role']=='user' else 'Assistant'} [{m.get('ts','')}]: {m['content']}"
                        for m in st.session_state.qa_messages
                    ),
                    file_name="research_chat.txt",
                    mime="text/plain",
                    key="dl_chat",
                )
            with c2:
                if st.button("🗑 Clear chat", key="clr_chat"):
                    st.session_state.qa_messages = []
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Input ─────────────────────────────────────────────────────────────
        q_col, btn_col = st.columns([5, 1])
        with q_col:
            question = st.text_input(
                label="YOUR QUESTION",
                placeholder="Ask anything about your papers, methodology, findings, comparisons…",
                key="qa_input_field",
            )
        with btn_col:
            st.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
            ask_clicked = st.button("Ask ➤", use_container_width=True, key="ask_btn")

        # Resolve question to submit
        pending_q = st.session_state.get("qa_pending", "")
        if pending_q:
            del st.session_state["qa_pending"]
            final_q = pending_q
        elif ask_clicked and question.strip():
            final_q = question.strip()
        else:
            final_q = None

        # ── Generate answer ───────────────────────────────────────────────────
        if final_q:
            now = datetime.datetime.now().strftime("%H:%M")
            st.session_state.qa_messages.append({"role": "user", "content": final_q, "ts": now})

            with st.spinner("Searching papers and composing answer…"):
                all_db_papers = get_all_papers()
                if all_db_papers:
                    per_paper_budget = max(400, 3500 // len(all_db_papers))
                    paper_blocks = []
                    for p in all_db_papers:
                        row = get_paper_by_id(p["id"])
                        if row:
                            snippet = " ".join(row["content"].split()[:per_paper_budget])
                            paper_blocks.append(
                                f"=== PAPER: {row['title']} (uploaded {row['uploaded_at']}) ===\n{snippet}"
                            )
                    combined_context = "\n\n".join(paper_blocks)
                    system_prompt = f"""You are a world-class research assistant and academic expert with deep knowledge across all scientific and scholarly domains.
You have access to a personal research library containing the papers listed below.

YOUR RESPONSIBILITIES:
- Answer the user's question with depth, precision, and scholarly rigour.
- Always ground your answer in the paper(s) provided when relevant — cite which paper each point comes from.
- If the question spans multiple papers, synthesise across them, highlighting agreements and contradictions.
- If the question goes beyond what the papers cover, clearly say so, then answer from your general expertise.
- Never give superficial or generic answers. Always go deep.

ANSWER FORMAT GUIDELINES:
- Start with a direct, concise answer to the question (2–3 sentences).
- Then elaborate with structured detail using headers or bullet points as appropriate.
- Include specific evidence: numbers, methods, findings from the papers where relevant.
- End with a brief synthesis or implication statement if the question warrants it.
- Use formal but accessible academic language.

--- RESEARCH LIBRARY ---
{combined_context}
--- END OF LIBRARY ---

Remember: cite which paper each piece of information comes from. Be thorough and analytical."""
                else:
                    system_prompt = """You are a world-class research assistant and academic expert with deep knowledge across all scientific and scholarly domains.

Answer the user's research question with depth, precision, and scholarly rigour.
- Start with a direct answer, then elaborate with structured detail.
- Use headers, bullet points, and numbered lists where appropriate.
- Include specific examples, evidence, methodologies, or theoretical frameworks where relevant.
- End with implications or further considerations.
- Use formal but accessible academic language. Never give generic or surface-level answers."""

                recent_msgs = st.session_state.qa_messages[-12:]
                lc_messages = [HumanMessage(content=system_prompt)]
                for m in recent_msgs:
                    lc_messages.append(
                        HumanMessage(content=m["content"]) if m["role"] == "user"
                        else AIMessage(content=m["content"])
                    )
                try:
                    answer_text = suggest_model.invoke(lc_messages).content
                except Exception as e:
                    answer_text = f"⚠️ Error: {str(e)}"

            ans_ts = datetime.datetime.now().strftime("%H:%M")
            st.session_state.qa_messages.append({"role": "assistant", "content": answer_text, "ts": ans_ts})
            st.rerun()