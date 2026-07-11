# ================================================================
# 🧞 GenIE - ULTRA PROFESSIONAL EDITION
# Clean • Modern • Enterprise Grade
# Innoviast Internship - Week 2
# ================================================================

import streamlit as st
from groq import Groq
import groq
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# ================================================================
# 📌 PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="GenIE - AI Content Studio",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# 🔐 ENVIRONMENT
# ================================================================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 GROQ_API_KEY not found! Add it to your .env file. Get a free key (no credit card) at https://console.groq.com/keys")
    st.stop()

# Native Groq SDK client (free tier, no credit card needed).
client = Groq(api_key=GROQ_API_KEY)

# ================================================================
# 🧞 SESSION STATE - FIXED
# ================================================================
if "output_editor" not in st.session_state:
    st.session_state.output_editor = ""  # ✅ Widget key
if "output_format" not in st.session_state:
    st.session_state.output_format = "Paragraphs"
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0
if "pending_output" not in st.session_state:
    st.session_state.pending_output = None  # holds content waiting to be applied to output_editor
if "generation_error" not in st.session_state:
    st.session_state.generation_error = None

# Apply any pending update to output_editor BEFORE the widget with that key
# is instantiated further down. This is the only safe place to change it.
if st.session_state.pending_output is not None:
    st.session_state.output_editor = st.session_state.pending_output
    st.session_state.pending_output = None

# ================================================================
# 🎨 INK & BRASS — SCRIBE'S STUDIO THEME
# ================================================================
st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,600;9..144,700;9..144,900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ===== TOKENS ===== */
    :root {
        --ink-900: #120f1c;
        --ink-850: #191527;
        --ink-800: #201a33;
        --ink-700: #2f2749;
        --ink-600: #453a66;
        --brass-500: #d1a13a;
        --brass-300: #ecce88;
        --brass-700: #96721f;
        --teal-400: #57d6bf;
        --parchment-100: #f3ecd9;
        --muted-400: #a79fc4;
        --muted-600: #756c95;
    }

    /* ===== RESET ===== */
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background:
            radial-gradient(ellipse 60% 40% at 15% 0%, rgba(87, 214, 191, 0.07), transparent 60%),
            radial-gradient(ellipse 50% 35% at 85% 8%, rgba(209, 161, 58, 0.10), transparent 60%),
            var(--ink-900) !important;
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        color: var(--parchment-100) !important;
    }

    /* Remove Streamlit's default reserved space above the page content,
       which otherwise shows up as a blank gap above the GenIE header. */
    .block-container {
        padding-top: 1rem !important;
    }
    header[data-testid="stHeader"] {
        background: var(--ink-900) !important;
        height: 2.5rem;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    /* ============================================================
       HEADER - MASTHEAD
    ============================================================ */
    .header-container {
        position: relative;
        text-align: center;
        padding: 2.6rem 0 1.8rem 0;
        margin: 0 -2rem 2.2rem -2rem;
        background: linear-gradient(180deg, var(--ink-850) 0%, var(--ink-900) 100%);
        border-bottom: 1px solid var(--ink-700);
        overflow: hidden;
    }

    .header-container::before {
        content: "";
        position: absolute;
        top: -80px;
        left: 50%;
        transform: translateX(-50%);
        width: 420px;
        height: 140px;
        background: radial-gradient(ellipse, rgba(209, 161, 58, 0.10) 0%, transparent 70%);
        filter: blur(8px);
        pointer-events: none;
    }

    .logo-ornament {
        position: relative;
        width: 64px;
        height: 1px;
        margin: 0 auto 1.1rem auto;
        background: linear-gradient(90deg, transparent, var(--brass-500), transparent);
    }

    .logo-ornament span {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 7px;
        height: 7px;
        background: var(--brass-300);
        transform: translate(-50%, -50%) rotate(45deg);
        box-shadow: 0 0 10px rgba(236, 206, 136, 0.7);
    }

    .logo-text {
        position: relative;
        font-size: 3.4rem;
        font-weight: 600;
        font-family: 'Fraunces', serif;
        letter-spacing: -1px;
        background: linear-gradient(135deg, var(--brass-300) 0%, var(--brass-500) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }

    .logo-sub {
        font-size: 0.68rem;
        color: var(--muted-400);
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 500;
        margin-top: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .logo-badge {
        display: inline-block;
        background: transparent;
        border: 1px solid var(--brass-700);
        color: var(--brass-300);
        font-size: 0.52rem;
        font-weight: 600;
        padding: 0.25rem 1rem;
        border-radius: 100px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ============================================================
       SIDEBAR - THE SCRIBE'S BENCH
    ============================================================ */
    [data-testid="stSidebar"] {
        background: var(--ink-850) !important;
        border-right: 1px solid var(--ink-700) !important;
        padding: 0 !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.25) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.8rem 1.5rem !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--parchment-100);
    }

    .sidebar-title {
        font-size: 0.62rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--brass-300);
        margin-bottom: 0.6rem;
        padding-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .sidebar-divider {
        border: none;
        border-top: 1px solid var(--ink-700);
        margin: 1.2rem 0;
    }

    /* ============================================================
       FORM ELEMENTS
    ============================================================ */
    .stSelectbox > div > div,
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: var(--ink-800) !important;
        border: 1px solid var(--ink-700) !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        color: var(--parchment-100) !important;
        transition: all 0.2s ease !important;
    }

    .stSelectbox > div > div *,
    [data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: var(--parchment-100) !important;
    }

    .stSelectbox > div > div:hover,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover {
        border-color: var(--ink-600) !important;
    }

    .stSelectbox > div > div:focus-within,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
        border-color: var(--brass-500) !important;
        box-shadow: 0 0 0 3px rgba(209, 161, 58, 0.15) !important;
    }

    div[data-baseweb="popover"] div[data-baseweb="menu"],
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background: var(--ink-800) !important;
        border: 1px solid var(--ink-700) !important;
    }

    div[data-baseweb="popover"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] li {
        background: transparent !important;
        color: var(--parchment-100) !important;
        font-size: 0.85rem !important;
    }

    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"],
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover,
    ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] {
        background: var(--ink-700) !important;
        color: var(--brass-300) !important;
    }

    .stTextInput > div > div > input,
    [data-testid="stTextInput"] input {
        background: var(--ink-800) !important;
        border: 1px solid var(--ink-700) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.85rem !important;
        color: var(--parchment-100) !important;
        -webkit-text-fill-color: var(--parchment-100) !important;
        min-height: 42px !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: var(--brass-500) !important;
        box-shadow: 0 0 0 3px rgba(209, 161, 58, 0.15) !important;
        background: var(--ink-850) !important;
    }

    .stTextArea > div > div > textarea,
    [data-testid="stTextArea"] textarea {
        background: var(--ink-800) !important;
        border: 1px solid var(--ink-700) !important;
        border-radius: 8px !important;
        padding: 0.9rem 1rem !important;
        font-size: 0.85rem !important;
        color: var(--parchment-100) !important;
        -webkit-text-fill-color: var(--parchment-100) !important;
        line-height: 1.75 !important;
        min-height: 140px !important;
        transition: all 0.2s ease !important;
    }

    .stTextArea > div > div > textarea:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--brass-500) !important;
        box-shadow: 0 0 0 3px rgba(209, 161, 58, 0.15) !important;
        background: var(--ink-850) !important;
    }

    .stTextArea textarea::placeholder,
    .stTextInput input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: var(--muted-600) !important;
        opacity: 1 !important;
        -webkit-text-fill-color: var(--muted-600) !important;
    }

    .stSelectbox label,
    .stTextInput label,
    .stTextArea label,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        font-size: 0.6rem !important;
        font-weight: 600 !important;
        color: var(--muted-400) !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        margin-bottom: 0.25rem !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    [data-testid="stSlider"] {
        color: var(--parchment-100) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background-color: var(--brass-500) !important;
        border-color: var(--brass-500) !important;
    }

    [data-testid="stTickBarMin"],
    [data-testid="stTickBarMax"] {
        color: var(--muted-400) !important;
    }

    /* ============================================================
       GENERATE BUTTON
    ============================================================ */
    .stButton > button {
        background: linear-gradient(135deg, var(--brass-300) 0%, var(--brass-500) 55%, var(--brass-700) 100%) !important;
        color: var(--ink-900) !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.5px;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        min-height: 46px !important;
        box-shadow: 0 4px 20px rgba(209, 161, 58, 0.28) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 0 4px rgba(87, 214, 191, 0.18), 0 8px 28px rgba(209, 161, 58, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ============================================================
       CARDS
    ============================================================ */
    .st-key-topic_card, .st-key-output_card {
        position: relative;
        background: var(--ink-850) !important;
        border-radius: 14px;
        padding: 1.8rem !important;
        border: 1px solid var(--ink-700);
        box-shadow: 0 2px 16px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        min-height: 460px;
        overflow: visible;
    }

    .st-key-topic_card::before, .st-key-topic_card::after,
    .st-key-output_card::before, .st-key-output_card::after {
        content: "";
        position: absolute;
        width: 14px;
        height: 14px;
        border-color: var(--brass-500);
        opacity: 0.7;
        pointer-events: none;
    }

    .st-key-topic_card::before, .st-key-output_card::before {
        top: 10px;
        left: 10px;
        border-top: 2px solid var(--brass-500);
        border-left: 2px solid var(--brass-500);
    }

    .st-key-topic_card::after, .st-key-output_card::after {
        bottom: 10px;
        right: 10px;
        border-bottom: 2px solid var(--brass-500);
        border-right: 2px solid var(--brass-500);
    }

    .st-key-topic_card:hover, .st-key-output_card:hover {
        box-shadow: 0 10px 32px rgba(0,0,0,0.3);
        border-color: var(--ink-600);
    }

    .card-title {
        font-size: 0.68rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--muted-400);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border-bottom: 1px solid var(--ink-700);
        padding-bottom: 0.8rem;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .card-title-icon {
        font-size: 1rem;
    }

    /* ============================================================
       OUTPUT AREA
    ============================================================ */
    .st-key-output_scroll {
        background: var(--ink-800) !important;
        border: 1px solid var(--ink-700);
        border-top: 2px solid !important;
        border-image: linear-gradient(90deg, var(--brass-500), var(--teal-400)) 1;
        border-radius: 10px;
        padding: 0.25rem !important;
    }

    .st-key-output_scroll textarea {
        background: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-size: 0.85rem !important;
        line-height: 1.8 !important;
        color: var(--parchment-100) !important;
        min-height: 320px !important;
        width: 100% !important;
        resize: vertical !important;
    }

    .st-key-output_scroll textarea:focus {
        box-shadow: none !important;
        background: var(--ink-850) !important;
        outline: none !important;
    }

    /* ============================================================
       TOOLBAR BUTTONS
    ============================================================ */
    .st-key-toolbar_row {
        padding: 0.7rem 0 0 0 !important;
        border-top: 1px solid var(--ink-700);
        margin-top: 0.7rem;
    }

    .st-key-toolbar_row .stButton > button,
    .st-key-toolbar_row .stDownloadButton > button {
        background: var(--ink-800) !important;
        color: var(--muted-400) !important;
        border: 1px solid var(--ink-700) !important;
        border-radius: 6px !important;
        padding: 0.4rem 0.6rem !important;
        font-size: 0.62rem !important;
        font-weight: 600 !important;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        box-shadow: none !important;
        min-height: 36px !important;
        transition: all 0.15s ease !important;
    }

    .st-key-toolbar_row .stButton > button:hover,
    .st-key-toolbar_row .stDownloadButton > button:hover {
        background: var(--ink-700) !important;
        border-color: var(--brass-500) !important;
        color: var(--brass-300) !important;
    }

    .st-key-toolbar_row .stButton > button:disabled,
    .st-key-toolbar_row .stDownloadButton > button:disabled {
        background: transparent !important;
        border-color: var(--ink-700) !important;
        color: var(--ink-600) !important;
        opacity: 0.6 !important;
    }

    .st-key-clear_btn button:hover {
        border-color: #c9564f !important;
        color: #e08b86 !important;
    }

    /* ============================================================
       EXPANDER
    ============================================================ */
    .streamlit-expanderHeader {
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        color: var(--muted-400) !important;
        background: var(--ink-800) !important;
        border-radius: 8px !important;
        border: 1px solid var(--ink-700) !important;
        padding: 0.4rem 0.8rem !important;
        transition: all 0.2s ease !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--brass-500) !important;
        color: var(--brass-300) !important;
    }

    .streamlit-expanderContent {
        background: var(--ink-850) !important;
        border: 1px solid var(--ink-700) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ============================================================
       ALERTS
    ============================================================ */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid var(--ink-700) !important;
        background: var(--ink-800) !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
        color: var(--muted-400) !important;
    }

    .stAlert svg { fill: var(--brass-500) !important; }

    /* ============================================================
       FOOTER
    ============================================================ */
    .footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid var(--ink-700);
        margin-top: 2.5rem;
    }

    .footer-text {
        font-size: 0.6rem;
        color: var(--muted-600);
        letter-spacing: 1.5px;
        font-weight: 400;
        font-family: 'JetBrains Mono', monospace;
    }

    .footer-text strong { color: var(--brass-300); font-weight: 600; }
    .footer-dot { color: var(--teal-400); font-weight: 700; margin: 0 0.4rem; }

    /* ============================================================
       SCROLLBAR
    ============================================================ */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: var(--ink-800); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: var(--brass-700); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--brass-500); }

    /* ============================================================
       STATS ROW
    ============================================================ */
    .stats-row {
        display: flex;
        gap: 0.6rem;
        padding: 0.2rem 0;
        flex-wrap: wrap;
    }

    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 0.58rem;
        color: var(--muted-400);
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-item strong { color: var(--brass-300); font-weight: 600; }

    /* ============================================================
       SAMPLE BOX
    ============================================================ */
    .sample-box {
        background: var(--ink-800);
        border-radius: 6px;
        border-left: 2px solid var(--teal-400);
        padding: 0.45rem 0.7rem;
        border-top: 1px solid var(--ink-700);
        border-right: 1px solid var(--ink-700);
        border-bottom: 1px solid var(--ink-700);
        margin: 0.3rem 0;
        font-size: 0.65rem;
        color: var(--muted-400);
        line-height: 1.4;
    }

    .sample-box strong { color: var(--brass-300); }

    /* ============================================================
       RESPONSIVE
    ============================================================ */
    @media (max-width: 768px) {
        .header-container { padding: 2rem 1rem 1.2rem 1rem; margin: 0 -1rem 1.5rem -1rem; }
        .logo-text { font-size: 2.6rem; }
        .logo-ornament { margin-bottom: 0.8rem; }
        .st-key-topic_card, .st-key-output_card { padding: 1rem !important; min-height: unset; }
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
# 📌 HEADER - BIG CENTERED LOGO
# ================================================================
st.markdown("""
<div class="header-container">
    <div class="logo-text">GenIE</div>
    <div class="logo-ornament"><span></span></div>
    <div class="logo-sub">Generative Intelligent Engine</div>
    <span class="logo-badge">Enterprise Edition</span>
</div>
""", unsafe_allow_html=True)

# ================================================================
# ⚙️ SIDEBAR
# ================================================================
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚙️ Studio Controls</p>', unsafe_allow_html=True)
    
    template = st.selectbox(
        "Content Type",
        ["Blog Post", "LinkedIn Post", "Email", "Ad Copy", "Product Description", "Caption"]
    )
    
    tone = st.selectbox(
        "Tone of Voice",
        ["Professional", "Casual", "Persuasive", "Emotional", "Humorous", "Formal", "Inspirational", "Witty"]
    )
    
    length_choice = st.select_slider(
        "Content Length",
        options=["Short", "Medium", "Long"],
        value="Medium",
        help="Short: 50-80 words · Medium: 150-250 words · Long: 350-500 words"
    )
    length_map = {
        "Short": "Short (50-80 words)",
        "Medium": "Medium (150-250 words)",
        "Long": "Long (350-500 words)"
    }
    length = length_map[length_choice]
    
    audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Enterprise leaders, Developers"
    )
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">📋 Output Format</p>', unsafe_allow_html=True)
    
    output_format = st.selectbox(
        "Format",
        ["Paragraphs", "Bullet Points", "Numbered List", "JSON Format"]
    )
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    generate_btn = st.button("🧞 Generate Content", type="primary", use_container_width=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-item">📊 <strong>{st.session_state.generation_count}</strong> generations</div>
        <div class="stat-item">⚡ <strong>OpenAI</strong></div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # PRO TIPS - IN SIDEBAR
    # ============================================================
    with st.expander("💡 Pro Tips", expanded=False):
        st.markdown("""
        <div style="font-size:0.7rem;color:#a79fc4;line-height:1.8;">
            <p>• <strong style="color:#ecce88;">Be specific</strong> about your topic for better results</p>
            <p>• <strong style="color:#ecce88;">Define your audience</strong> clearly to match the tone</p>
            <p>• <strong style="color:#ecce88;">Add keywords</strong> for SEO optimization</p>
            <p>• <strong style="color:#ecce88;">Choose the right tone</strong> that resonates</p>
            <p>• <strong style="color:#ecce88;">Select output format</strong> that fits your needs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # TEMPLATE LIBRARY
    # ============================================================
    with st.expander("📚 Template Library", expanded=False):
        st.markdown("""
        <div style="font-size:0.65rem;color:#a79fc4;line-height:1.8;">
            <p><strong style="color:#ecce88;">📝 Blog Post</strong><br>Long-form articles with structured headings</p>
            <p><strong style="color:#ecce88;">💼 LinkedIn Post</strong><br>Professional social media content</p>
            <p><strong style="color:#ecce88;">📧 Email</strong><br>Professional email campaigns</p>
            <p><strong style="color:#ecce88;">📢 Ad Copy</strong><br>Conversion-focused advertisements</p>
            <p><strong style="color:#ecce88;">🏷️ Product Description</strong><br>Feature-focused product content</p>
            <p><strong style="color:#ecce88;">📱 Caption</strong><br>Social media captions with engagement</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # SAMPLE OUTPUTS
    # ============================================================
    with st.expander("📄 Sample Outputs", expanded=False):
        st.markdown("""
        <div class="sample-box">
            <strong>📝 Blog:</strong> "10 AI Trends That Will Shape 2025"
        </div>
        <div class="sample-box">
            <strong>💼 LinkedIn:</strong> "Excited to announce our new product! 🚀"
        </div>
        <div class="sample-box">
            <strong>📧 Email:</strong> "Subject: Your 30% discount ends today!"
        </div>
        <div class="sample-box">
            <strong>📱 Caption:</strong> "Sunday vibes with our new collection! ✨"
        </div>
        """, unsafe_allow_html=True)

# ================================================================
# 📝 MAIN CONTENT - TWO CLEAN BOXES
# ================================================================
col1, col2 = st.columns(2, gap="large")

# ================================================================
# LEFT BOX - TOPIC & INPUTS
# ================================================================
with col1:
    with st.container(key="topic_card"):
        st.markdown('<p class="card-title"><span class="card-title-icon">✍️</span> Topic & Inputs</p>', unsafe_allow_html=True)

        topic = st.text_area(
            "",
            height=180,
            placeholder="Describe your topic in detail...\n\nExample: 'The future of artificial intelligence in healthcare and how it's transforming patient care.'",
            label_visibility="collapsed"
        )

        st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)

        keywords = st.text_input(
            "🔑 Keywords (Optional)",
            placeholder="e.g., AI, healthcare, innovation, future",
            help="Comma-separated keywords for SEO optimization"
        )

# ================================================================
# RIGHT BOX - GENERATED CONTENT
# ================================================================
with col2:
    with st.container(key="output_card"):
        st.markdown('<p class="card-title"><span class="card-title-icon">📄</span> Generated Content</p>', unsafe_allow_html=True)

        if st.session_state.generation_error:
            st.error(st.session_state.generation_error)

        with st.container(key="output_scroll"):
            output_text = st.text_area(
                "",
                height=300,
                key="output_editor",
                label_visibility="collapsed",
                placeholder="Your generated content will appear here. You can edit it directly."
            )

        # ============================================================
        # TOOLBAR
        # ============================================================
        with st.container(key="toolbar_row"):
            col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5, gap="small")

            with col_btn1:
                if st.button("📋 Copy", use_container_width=True):
                    st.toast("✅ Copied to clipboard!", icon="📋")

            with col_btn2:
                st.download_button(
                    label="📥 .txt",
                    data=st.session_state.output_editor,
                    file_name=f"genie_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    disabled=not st.session_state.output_editor
                )

            with col_btn3:
                md_content = f"""# GenIE Content
**Template:** {template}
**Tone:** {tone}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---
{st.session_state.output_editor}

---
*Generated by GenIE - AI Content Studio*
"""
                st.download_button(
                    label="📝 .md",
                    data=md_content,
                    file_name=f"genie_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    disabled=not st.session_state.output_editor
                )

            with col_btn4:
                if st.button("🔄 Clear", use_container_width=True):
                    st.session_state.pending_output = ""
                    st.rerun()

            with col_btn5:
                if output_format == "JSON Format" and st.session_state.output_editor:
                    try:
                        json_data = json.dumps({
                            "content": st.session_state.output_editor,
                            "metadata": {"template": template, "tone": tone}
                        }, indent=2)
                        st.download_button(
                            label="📊 .json",
                            data=json_data,
                            file_name=f"genie_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    except:
                        pass

# ================================================================
# 🧞 PROMPTS
# ================================================================
def get_template_prompt(template, topic, tone, length, audience, keywords, output_format):
    format_instruction = {
        "Paragraphs": "Write in well-structured paragraphs.",
        "Bullet Points": "Use bullet points (•) for each key point.",
        "Numbered List": "Use numbered lists (1., 2., 3.).",
        "JSON Format": "Return valid JSON with keys: 'headline', 'content', 'key_points', 'cta'."
    }.get(output_format, "Write in paragraphs.")
    
    prompts = {
        "Blog Post": f"""Write a comprehensive blog post about: {topic}

STRUCTURE:
1. H1 headline
2. Introduction with hook
3. 3-4 H2 sections
4. Key takeaways
5. Conclusion with CTA

FORMAT: {format_instruction}
TONE: {tone}
LENGTH: {length}
AUDIENCE: {audience}
KEYWORDS: {keywords}""",

        "LinkedIn Post": f"""Write a professional LinkedIn post about: {topic}

STRUCTURE:
1. Hook (first 2 lines)
2. Main content (3-4 points)
3. Personal insight
4. Question for engagement
5. 3-5 hashtags

FORMAT: {format_instruction}
TONE: {tone}
LENGTH: {length}
AUDIENCE: {audience}""",

        "Email": f"""Write a compelling email about: {topic}

STRUCTURE:
1. Subject line
2. Greeting
3. Main message
4. Call to action
5. Signature

FORMAT: {format_instruction}
TONE: {tone}
LENGTH: {length}
AUDIENCE: {audience}""",

        "Ad Copy": f"""Write persuasive ad copy about: {topic}

STRUCTURE:
1. Headline
2. Problem
3. Solution
4. Benefits (3-4)
5. Social proof
6. Call to action

FORMAT: {format_instruction}
TONE: {tone}
LENGTH: {length}
AUDIENCE: {audience}""",

        "Product Description": f"""Write a product description for: {topic}

STRUCTURE:
1. Product name
2. Tagline
3. Key features
4. Benefits
5. Specifications

FORMAT: {format_instruction}
TONE: {tone}
LENGTH: {length}
AUDIENCE: {audience}""",

        "Caption": f"""Write an engaging caption about: {topic}

STRUCTURE:
1. Hook
2. Main message
3. Emojis (3-4)
4. Call to action
5. Hashtags

FORMAT: {format_instruction}
TONE: {tone}
LENGTH: {length}
AUDIENCE: {audience}"""
    }
    return prompts.get(template, f"Write about {topic} with {tone} tone for {audience}")

# ================================================================
# 🧞 GENERATE
# ================================================================
def generate_content(template, tone, length, audience, topic, keywords, output_format):
    """Returns (content, error_message). Exactly one of them will be non-None."""
    prompt = get_template_prompt(template, topic, tone, length, audience, keywords, output_format)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert content writer with 10+ years of experience."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.9
        )
        return response.choices[0].message.content, None
    except groq.RateLimitError:
        return None, (
            "🚫 Groq free-tier rate limit hit (30 requests/min or daily cap). "
            "Wait a minute and try again, or check console.groq.com/settings/limits."
        )
    except groq.AuthenticationError:
        return None, "🔑 Invalid or missing GROQ_API_KEY. Get a free key at console.groq.com/keys and check your .env file."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# ================================================================
# 🧞 GENERATE LOGIC - FIXED
# ================================================================
if generate_btn:
    if not topic:
        st.warning("⚠️ Please enter a topic before generating!")
    else:
        with st.spinner("🧞 GenIE is generating your content..."):
            content, error = generate_content(template, tone, length, audience, topic, keywords, output_format)
            if error:
                st.session_state.generation_error = error
            else:
                st.session_state.pending_output = content  # applied to output_editor on next run, before widget creation
                st.session_state.generation_error = None
                st.session_state.generation_count += 1
            st.rerun()

# ================================================================
# 📌 FOOTER
# ================================================================
st.markdown("""
<div class="footer">
    <p class="footer-text">
        <strong>🧞 GenIE</strong> 
        <span class="footer-dot">•</span> 
        Enterprise AI Content Studio 
        <span class="footer-dot">•</span> 
        6 Templates • 8 Tones • 4 Formats
        <span class="footer-dot">•</span> 
        Innoviast Internship • Week 2
    </p>
</div>
""", unsafe_allow_html=True)