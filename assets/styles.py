"""
assets/styles.py
Returns the full CSS string injected via st.markdown.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:          #080d14;
    --bg2:         #0f1823;
    --bg3:         #162030;
    --bg4:         #1c2b3f;
    --gold:        #f0b429;
    --gold-soft:   #f5c842;
    --gold-dim:    rgba(240,180,41,0.10);
    --gold-border: rgba(240,180,41,0.25);
    --teal:        #34d399;
    --teal-dim:    rgba(52,211,153,0.08);
    --teal-border: rgba(52,211,153,0.25);
    --rose:        #fb7185;
    --violet:      #a78bfa;
    --text:        #e2e8f0;
    --text2:       #94a3b8;
    --muted:       #4a5568;
    --border:      #1a2d40;
    --border2:     #243852;
    --radius:      12px;
    --radius-sm:   8px;
    --shadow:      0 4px 24px rgba(0,0,0,0.4);
    --shadow-sm:   0 2px 8px rgba(0,0,0,0.25);
}

@keyframes fadeUp   { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn   { from{opacity:0} to{opacity:1} }
@keyframes slideIn  { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:translateX(0)} }

html,body,[class*="css"]{ font-family:'DM Sans',system-ui,sans-serif!important;background:var(--bg)!important;color:var(--text)!important; }
.stApp{ background:var(--bg)!important; }
.block-container{ padding-top:1.2rem!important;max-width:980px!important;animation:fadeIn 0.4s ease; }

::-webkit-scrollbar{ width:4px;height:4px; }
::-webkit-scrollbar-track{ background:transparent; }
::-webkit-scrollbar-thumb{ background:var(--border2);border-radius:4px; }
::-webkit-scrollbar-thumb:hover{ background:var(--muted); }

[data-testid="stSidebar"]{ background:var(--bg2)!important;border-right:1px solid var(--border)!important; }
[data-testid="stSidebar"]>div:first-child{ padding-top:1.5rem!important; }

.app-header{ display:flex;align-items:center;gap:1rem;padding:0.8rem 0 1.2rem;border-bottom:1px solid var(--border);margin-bottom:1.4rem;animation:fadeUp 0.5s ease; }
.app-header-icon{ width:46px;height:46px;background:linear-gradient(135deg,var(--gold-dim),rgba(240,180,41,0.05));border:1px solid var(--gold-border);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0;box-shadow:0 0 20px rgba(240,180,41,0.1); }
.app-header h1{ font-family:'DM Serif Display',Georgia,serif!important;font-size:1.7rem!important;font-weight:400!important;color:var(--text)!important;margin:0!important;line-height:1.2;letter-spacing:-0.3px; }
.app-header p{ margin:0.25rem 0 0!important;font-size:0.8rem!important;color:var(--text2)!important;font-weight:300!important; }

.stTabs [data-baseweb="tab-list"]{ background:var(--bg2)!important;border-radius:var(--radius)!important;padding:4px!important;gap:2px!important;border:1px solid var(--border)!important;animation:fadeIn 0.4s ease 0.15s both; }
.stTabs [data-baseweb="tab"]{ background:transparent!important;color:var(--text2)!important;border-radius:var(--radius-sm)!important;font-family:'DM Sans',sans-serif!important;font-size:0.85rem!important;font-weight:500!important;padding:0.5rem 1.2rem!important;border:none!important;transition:color 0.18s,background 0.18s!important; }
.stTabs [data-baseweb="tab"]:hover{ color:var(--text)!important;background:var(--bg3)!important; }
.stTabs [aria-selected="true"]{ background:var(--bg4)!important;color:var(--gold)!important;box-shadow:0 1px 8px rgba(0,0,0,0.4),0 0 0 1px rgba(240,180,41,0.1)!important; }
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{ display:none!important; }

.stTextInput input,.stTextArea textarea{ background:var(--bg2)!important;border:1.5px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;font-size:0.95rem!important;padding:0.7rem 1rem!important;transition:border-color 0.2s,box-shadow 0.2s!important; }
.stTextInput input:focus,.stTextArea textarea:focus{ border-color:var(--gold)!important;box-shadow:0 0 0 3px rgba(240,180,41,0.1)!important;outline:none!important; }
.stTextInput>label,.stTextArea>label,.stSelectbox>label{ font-family:'JetBrains Mono',monospace!important;font-size:0.7rem!important;color:var(--muted)!important;letter-spacing:1px!important;text-transform:uppercase!important;margin-bottom:6px!important; }

.stSelectbox [data-baseweb="select"]>div:first-child{ background:var(--bg2)!important;border:1.5px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;transition:border-color 0.2s!important; }
.stSelectbox [data-baseweb="select"]>div:first-child:focus-within{ border-color:var(--gold)!important;box-shadow:0 0 0 3px rgba(240,180,41,0.1)!important; }

.stRadio>div{ gap:0.5rem!important; }
.stRadio label{ background:var(--bg2)!important;border:1.5px solid var(--border)!important;border-radius:var(--radius-sm)!important;padding:0.45rem 1.1rem!important;color:var(--text2)!important;font-size:0.85rem!important;cursor:pointer!important;transition:all 0.18s!important; }
.stRadio label:hover{ border-color:var(--border2)!important;color:var(--text)!important; }
.stRadio label:has(input:checked){ border-color:var(--gold-border)!important;background:var(--gold-dim)!important;color:var(--gold)!important;box-shadow:0 0 0 1px var(--gold-border)!important; }

.stButton>button{ background:linear-gradient(135deg,#f0b429 0%,#c98f0a 100%)!important;color:#08100a!important;font-family:'DM Sans',sans-serif!important;font-size:0.88rem!important;font-weight:600!important;letter-spacing:0.2px!important;border:none!important;border-radius:var(--radius)!important;padding:0.6rem 1.5rem!important;transition:transform 0.15s,box-shadow 0.15s!important;box-shadow:0 2px 10px rgba(240,180,41,0.3)!important; }
.stButton>button:hover{ transform:translateY(-2px)!important;box-shadow:0 6px 22px rgba(240,180,41,0.45)!important; }
.stButton>button:active{ transform:translateY(0)!important;box-shadow:0 2px 8px rgba(240,180,41,0.2)!important; }

[data-testid="stFileUploader"]{ background:var(--bg2)!important;border:2px dashed var(--border)!important;border-radius:var(--radius)!important;transition:border-color 0.2s,background 0.2s!important; }
[data-testid="stFileUploader"]:hover{ border-color:var(--gold-border)!important;background:var(--gold-dim)!important; }

details{ background:var(--bg2)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;overflow:hidden!important;transition:border-color 0.2s!important;margin-bottom:6px!important; }
details:hover,details[open]{ border-color:var(--border2)!important; }
details summary{ padding:0.8rem 1.1rem!important;font-size:0.88rem!important;color:var(--text)!important;cursor:pointer!important;transition:background 0.15s!important;user-select:none; }
details summary:hover{ background:var(--bg3)!important; }

.stAlert{ border-radius:var(--radius)!important;font-size:0.87rem!important;animation:fadeUp 0.3s ease!important; }
.stSpinner>div{ border-top-color:var(--gold)!important; }
hr{ border-color:var(--border)!important;margin:1.2rem 0!important; }

/* ── Custom components ─────────────────────────────────────── */
.metric-row{ display:flex;gap:7px;margin:0.9rem 0;flex-wrap:wrap;animation:fadeIn 0.4s ease; }
.metric-chip{ background:var(--bg3);border:1px solid var(--border);border-radius:20px;padding:4px 12px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--text2);white-space:nowrap;transition:border-color 0.15s; }
.metric-chip span{ color:var(--teal);font-weight:600; }
.metric-chip.gold{ border-color:var(--gold-border);color:var(--gold);background:var(--gold-dim); }
.metric-chip.teal{ border-color:var(--teal-border);color:var(--teal);background:var(--teal-dim); }

.mode-badge{ display:inline-flex;align-items:center;gap:5px;padding:3px 11px;border-radius:20px;font-size:0.73rem;font-family:'JetBrains Mono',monospace;font-weight:500;letter-spacing:0.4px; }
.badge-summarize{ background:var(--gold-dim);color:var(--gold);border:1px solid var(--gold-border); }
.badge-findings{ background:var(--teal-dim);color:var(--teal);border:1px solid var(--teal-border); }
.badge-review{ background:rgba(251,113,133,0.08);color:var(--rose);border:1px solid rgba(251,113,133,0.22); }
.badge-suggest{ background:rgba(167,139,250,0.08);color:var(--violet);border:1px solid rgba(167,139,250,0.22); }

.result-card{ background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--gold);border-radius:var(--radius);padding:1.4rem 1.6rem;margin-top:0.9rem;line-height:1.85;font-size:0.93rem;animation:fadeUp 0.5s ease;box-shadow:var(--shadow-sm); }

.chat-wrap{ animation:fadeUp 0.35s ease; }
.chat-user{ display:flex;justify-content:flex-end;margin-bottom:0.9rem; }
.chat-user-inner{ display:flex;flex-direction:column;align-items:flex-end;gap:3px; }
.chat-user-bubble{ background:var(--bg4);border:1px solid var(--border2);border-radius:16px 16px 3px 16px;padding:0.75rem 1.1rem;max-width:76%;font-size:0.93rem;line-height:1.65;color:var(--text);box-shadow:var(--shadow-sm); }
.chat-ts{ font-size:0.68rem;color:var(--muted);font-family:'JetBrains Mono',monospace;padding:0 4px; }
.chat-bot{ display:flex;justify-content:flex-start;align-items:flex-start;gap:0.65rem;margin-bottom:0.9rem; }
.chat-bot-avatar{ width:32px;height:32px;flex-shrink:0;background:linear-gradient(135deg,var(--gold-dim),rgba(240,180,41,0.04));border:1px solid var(--gold-border);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;margin-top:3px; }
.chat-bot-inner{ display:flex;flex-direction:column;gap:3px;max-width:82%; }
.chat-bot-bubble{ background:var(--bg2);border:1px solid var(--border);border-radius:3px 16px 16px 16px;padding:0.8rem 1.1rem;font-size:0.93rem;line-height:1.78;color:var(--text);box-shadow:var(--shadow-sm); }

.banner{ border-radius:var(--radius);padding:0.7rem 1rem;margin-bottom:1rem;font-size:0.83rem;font-family:'DM Sans',sans-serif;display:flex;align-items:center;gap:0.6rem;animation:fadeIn 0.3s ease; }
.banner-teal{ background:var(--teal-dim);border:1px solid var(--teal-border);color:var(--teal); }
.banner-gold{ background:var(--gold-dim);border:1px solid var(--gold-border);color:var(--gold); }
.banner-muted{ background:var(--bg3);border:1px solid var(--border);color:var(--text2); }

.sub-label{ font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.1px;margin-bottom:0.5rem;display:block; }

.agent-card{ background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.6rem 0.85rem;margin-bottom:0.4rem;display:flex;align-items:center;gap:0.65rem;transition:border-color 0.15s,transform 0.15s;cursor:default; }
.agent-card:hover{ border-color:var(--border2);transform:translateX(2px); }
.agent-card-icon{ font-size:1rem;flex-shrink:0; }
.agent-card-name{ font-size:0.82rem;font-weight:500;color:var(--text); }
.agent-card-desc{ font-size:0.72rem;color:var(--muted);margin-top:1px; }

.sb-stat{ background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.55rem 0.9rem;margin-bottom:0.4rem;display:flex;justify-content:space-between;align-items:center; }
.sb-stat-label{ font-size:0.77rem;color:var(--text2); }
.sb-stat-value{ font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:var(--gold);font-weight:500; }

.mode-desc{ background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.65rem 0.9rem;font-size:0.83rem;color:var(--text2);margin-bottom:1rem;display:flex;align-items:flex-start;gap:0.5rem;animation:fadeIn 0.25s ease; }
.preview-block{ background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.9rem 1rem;font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:var(--text2);max-height:220px;overflow-y:auto;white-space:pre-wrap;line-height:1.6; }

.paper-card{ background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.2rem;margin-bottom:0.6rem;transition:border-color 0.2s,box-shadow 0.2s,transform 0.2s;animation:fadeUp 0.35s ease; }
.paper-card:hover{ border-color:var(--gold-border);box-shadow:0 4px 20px rgba(240,180,41,0.07);transform:translateY(-1px); }
.paper-card-title{ font-family:'DM Serif Display',serif;font-size:0.98rem;color:var(--text);margin-bottom:0.35rem;line-height:1.3; }
.paper-card-meta{ font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;margin-top:0.2rem; }
.paper-card-meta span{ display:flex;align-items:center;gap:4px; }

.empty-state{ text-align:center;padding:3rem 2rem;background:var(--bg2);border:2px dashed var(--border);border-radius:var(--radius);color:var(--text2);animation:fadeIn 0.4s ease; }
.empty-state-icon{ font-size:2.5rem;margin-bottom:0.8rem;display:block; }
.empty-state-title{ font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--text);margin-bottom:0.4rem; }
.empty-state-desc{ font-size:0.83rem;color:var(--text2); }
</style>
"""