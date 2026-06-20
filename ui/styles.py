import streamlit as st


def apply_styles():
    st.markdown('''
    <style>
    :root { --bg:#070b12; --card:#101827; --soft:#172033; --text:#e5edf8; --muted:#8ea3bd; --line:#26354d; --green:#18c37e; --yellow:#f7b731; --red:#ff5a5f; --blue:#4da3ff; }
    .stApp { background: radial-gradient(circle at top left,#10203a 0,#070b12 38%,#05070b 100%); color: var(--text); }
    h1,h2,h3,h4,p,span,div,label { color: var(--text); }
    [data-testid="stSidebar"] { background:#080d15; border-right:1px solid #1a2740; }
    .hero { padding:24px; border-radius:24px; background:linear-gradient(135deg,#101827,#0b1220); border:1px solid #26354d; box-shadow:0 18px 45px rgba(0,0,0,.35); }
    .tiny { color:#8ea3bd !important; font-size:13px; }
    .card { background:rgba(16,24,39,.94); border:1px solid #26354d; border-radius:22px; padding:22px; box-shadow:0 14px 34px rgba(0,0,0,.28); }
    .decision { border-radius:28px; padding:32px; text-align:center; border:2px solid #26354d; box-shadow:0 20px 60px rgba(0,0,0,.4); }
    .decision-green { background:linear-gradient(135deg,#0b2f23,#102418); border-color:#18c37e; }
    .decision-yellow { background:linear-gradient(135deg,#3a2b0b,#1e1a10); border-color:#f7b731; }
    .decision-red { background:linear-gradient(135deg,#3a1116,#1e1012); border-color:#ff5a5f; }
    .decision-title { font-size:44px; font-weight:950; letter-spacing:.5px; }
    .decision-sub { font-size:18px; color:#cbd5e1 !important; margin-top:8px; }
    .pill { display:inline-block; padding:8px 12px; border-radius:999px; background:#172033; border:1px solid #26354d; font-weight:800; margin:3px; }
    .metricbox { background:#0d1524; border:1px solid #26354d; border-radius:18px; padding:18px; text-align:center; min-height:110px; }
    .metric-label { color:#8ea3bd !important; font-size:13px; font-weight:800; }
    .metric-value { font-size:30px; font-weight:950; margin-top:7px; }
    .good { color:#18c37e !important; } .warn { color:#f7b731 !important; } .bad { color:#ff5a5f !important; } .blue { color:#4da3ff !important; }
    .explain { background:#0d1524; border-left:5px solid #4da3ff; border-radius:16px; padding:18px; margin:10px 0; }
    .ytd { background:#271316; border:1px solid #ff5a5f; color:#ffd7d9 !important; padding:14px; border-radius:14px; font-weight:800; }
    .placeholder { background:#0d1524; border:1px dashed #45546b; border-radius:18px; padding:20px; color:#b8c7da !important; }
    div[data-testid="stMetricValue"] { font-weight:900; }
    .stButton button { border-radius:14px; font-weight:900; border:1px solid #334155; }
    /* v3.3 günlük trade adayları */
    .tradepick{
        background: linear-gradient(180deg, rgba(24,36,58,.98), rgba(12,20,34,.98));
        border:1px solid #29466f;
        border-radius:18px;
        padding:18px;
        min-height:150px;
        box-shadow:0 10px 24px rgba(0,0,0,.18);
        color:#f8fafc;
    }
    .tradepick b{color:#f8fafc; font-size:16px;}
    .tradepick span{color:#9cc7ff; font-size:13px;}
    .tradepick hr{border:0; border-top:1px solid rgba(148,163,184,.25); margin:10px 0;}
    .tradepick small{color:#fbbf24; font-weight:700;}
    </style>
    ''', unsafe_allow_html=True)

# v3.4 mobile tightening
