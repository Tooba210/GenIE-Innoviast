# ================================================================
# 🧞 GenIE - CORPORATE PROFESSIONAL UI (FULLY FIXED)
# No Extra Space • Professional Buttons
# Innoviast Internship - Week 2
# ================================================================

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# ================================================================
# 📌 PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="GenIE - Enterprise AI Studio",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# 🔐 ENVIRONMENT
# ================================================================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 GROQ_API_KEY not found! Please add it to your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ================================================================
# 🧞 SESSION STATE
# ================================================================
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "output_format" not in st.session_state:
    st.session_state.output_format = "Paragraphs"
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

# ================================================================
# 🎨 PROFESSIONAL CSS - NO EXTRA SPACE
# ================================================================
st.markdown("""
<style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #f5f7fa;
        --bg-secondary: #ffffff;
        --bg-card: #ffffff;
        --text-primary: #1a1a2e;
        --text-secondary: #4a4a6a;
        --text-muted: #8a8aaa;
        --border-color: #e8e8f0;
        --accent: #2563eb;
        --accent-light: #dbeafe;
        --accent-gradient: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.06);
        --radius-sm: 8px;
        --radius-md: 12px;
    }
    
    /* ===== GLOBAL ===== */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* ===== HEADER ===== */
    .header-wrapper {
        background: var(--bg-secondary);
        padding: 0.7rem 2.5rem;
        border-bottom: 1px solid var(--border-color);
        margin: -1rem -2rem 1.5rem -2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        box-shadow: var(--shadow-sm);
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    
    .header-logo {
        background: var(--accent-gradient);
        color: white;
        width: 34px;
        height: 34px;
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.9rem;
    }
    
    .header-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.3px;
    }
    
    .header-title span {
        color: var(--accent);
    }
    
    .header-badge {
        background: var(--accent-light);
        color: var(--accent);
        padding: 0.15rem 0.7rem;
        border-radius: 100px;
        font-size: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .header-tags {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        flex-wrap: wrap;
    }
    
    .tag {
        background: var(--bg-primary);
        padding: 0.15rem 0.7rem;
        border-radius: 100px;
        font-size: 0.55rem;
        font-weight: 500;
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
    }
    
    .tag-accent {
        background: var(--accent);
        color: white;
        border-color: var(--accent);
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.2rem 1rem !important;
    }
    
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .sidebar-brand-icon {
        background: var(--accent-gradient);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1rem;
    }
    
    .sidebar-brand-text {
        font-weight: 700;
        font-size: 1rem;
        color: var(--text-primary);
    }
    
    .sidebar-brand-text span {
        color: var(--accent);
    }
    
    .sidebar-brand-sub {
        font-size: 0.45rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sidebar-label {
        font-size: 0.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-muted) !important;
        margin-bottom: 0.4rem !important;
        margin-top: 0.8rem !important;
    }
    
    /* ===== CARDS ===== */
    .card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.2rem;
        box-shadow: var(--shadow-sm);
        height: 100%;
    }
    
    .card-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-primary);
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.6rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .card-title-icon {
        color: var(--accent);
    }
    
    /* ===== FORM ELEMENTS ===== */
    .stSelectbox > div > div {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        min-height: 36px !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
    }
    
    .stTextInput > div > div > input {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem 0.8rem !important;
        font-size: 0.8rem !important;
        color: var(--text-primary) !important;
        min-height: 36px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
    }
    
    .stTextArea > div > div > textarea {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem 0.8rem !important;
        font-size: 0.8rem !important;
        color: var(--text-primary) !important;
        line-height: 1.6 !important;
        min-height: 100px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
    }
    
    .stSlider > div { padding: 0.2rem 0 !important; }
    
    /* ===== LABELS ===== */
    .stSelectbox label,
    .stTextInput label,
    .stTextArea label,
    .stSlider label {
        font-size: 0.55rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        margin-bottom: 0.15rem !important;
    }
    
    /* ===== GENERATE BUTTON ===== */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.3px;
        transition: all 0.2s ease !important;
        width: 100% !important;
        min-height: 40px !important;
        box-shadow: 0 2px 12px rgba(37, 99, 235, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* ===== OUTPUT AREA - COMPACT ===== */
    .output-container {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        padding: 0.25rem;
        min-height: 280px;
    }
    
    .output-container textarea {
        background: transparent !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem !important;
        font-size: 0.8rem !important;
        line-height: 1.7 !important;
        color: var(--text-primary) !important;
        min-height: 260px !important;
        width: 100% !important;
        resize: vertical !important;
    }
    
    .output-container textarea:focus {
        box-shadow: none !important;
        background: var(--bg-secondary) !important;
        outline: none !important;
    }
    
    /* ============================================================
       PROFESSIONAL TOOLBAR BUTTONS
    ============================================================ */
    .toolbar {
        display: flex;
        gap: 0.3rem;
        padding: 0.4rem 0 0 0;
        border-top: 1px solid var(--border-color);
        margin-top: 0.4rem;
        flex-wrap: wrap;
    }
    
    /* Professional Buttons - Clean & Minimal */
    .toolbar-btn > button {
        background: var(--bg-primary) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 0.25rem 0.6rem !important;
        font-size: 0.6rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        width: auto !important;
        min-width: 55px !important;
        min-height: 30px !important;
        transition: all 0.15s ease !important;
        letter-spacing: 0.2px !important;
        text-transform: none !important;
    }
    
    .toolbar-btn > button:hover {
        background: var(--accent-light) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1) !important;
    }
    
    .toolbar-btn > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Disabled state ke liye */
    .toolbar-btn > button:disabled {
        opacity: 0.4 !important;
        cursor: not-allowed !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        font-size: 0.65rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        background: var(--bg-primary) !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border-color) !important;
        padding: 0.3rem 0.7rem !important;
    }
    
    /* ===== ALERTS ===== */
    .stAlert {
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border-color) !important;
        background: var(--accent-light) !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.75rem !important;
        color: var(--text-secondary) !important;
    }
    
    /* ===== DIVIDER ===== */
    .sidebar-divider {
        border: none;
        border-top: 1px solid var(--border-color);
        margin: 0.8rem 0;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1rem 0 0.3rem 0;
        border-top: 1px solid var(--border-color);
        margin-top: 1.5rem;
    }
    
    .footer-text {
        font-size: 0.55rem;
        color: var(--text-muted);
        letter-spacing: 1px;
        font-weight: 400;
    }
    
    .footer-text strong { 
        color: var(--text-secondary); 
        font-weight: 600;
    }
    
    .footer-dot { 
        color: var(--accent); 
        font-weight: 700; 
        margin: 0 0.3rem; 
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }
    
    /* ===== STATS ===== */
    .stats-row {
        display: flex;
        gap: 0.6rem;
        padding: 0.2rem 0;
        flex-wrap: wrap;
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.2rem;
        font-size: 0.55rem;
        color: var(--text-muted);
    }
    
    .stat-item strong {
        color: var(--text-secondary);
        font-weight: 600;
    }
    
    /* ===== SAMPLE BOX ===== */
    .sample-box {
        background: var(--bg-primary);
        border-radius: var(--radius-sm);
        padding: 0.4rem 0.6rem;
        border: 1px solid var(--border-color);
        margin: 0.2rem 0;
        font-size: 0.65rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .sample-box strong { color: var(--accent); }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .header-wrapper { 
            padding: 0.6rem 1rem; 
            margin: -1rem -1rem 1rem -1rem;
        }
        .header-title { font-size: 0.9rem !important; }
        .header-badge { display: none; }
        .card { padding: 0.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
# 📌 HEADER
# ================================================================
st.markdown("""
<div class="header-wrapper">
    <div class="header-left">
        <div class="header-logo">◆</div>
        <div>
            <span class="header-title"><span>Gen</span>IE</span>
            <span class="header-badge">Enterprise</span>
        </div>
    </div>
    <div class="header-tags">
        <span class="tag tag-accent">⚡ Groq</span>
        <span class="tag">Llama 3.3</span>
        <span class="tag">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================
# ⚙️ SIDEBAR
# ================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">◆</div>
        <div>
            <div class="sidebar-brand-text"><span>Gen</span>IE</div>
            <div class="sidebar-brand-sub">Enterprise AI Studio</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-label">⚙️ Configuration</p>', unsafe_allow_html=True)
    
    template = st.selectbox(
        "Content Type",
        ["Blog Post", "LinkedIn Post", "Email", "Ad Copy", "Product Description", "Caption"]
    )
    
    tone = st.selectbox(
        "Tone of Voice",
        ["Professional", "Casual", "Persuasive", "Emotional", "Humorous", "Formal", "Inspirational", "Witty"]
    )
    
    length = st.select_slider(
        "Content Length",
        options=["Short (50-80 words)", "Medium (150-250 words)", "Long (350-500 words)"],
        value="Medium (150-250 words)"
    )
    
    audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Enterprise leaders, Developers"
    )
    
    st.markdown('<p class="sidebar-label" style="margin-top:1rem;">📋 Output</p>', unsafe_allow_html=True)
    
    output_format = st.selectbox(
        "Format",
        ["Paragraphs", "Bullet Points", "Numbered List", "JSON Format"]
    )
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    generate_btn = st.button("◆ Generate Content", type="primary", use_container_width=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-item">📊 <strong>{st.session_state.generation_count}</strong> generations</div>
        <div class="stat-item">⚡ <strong>Groq</strong> API</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📚 Template Library", expanded=False):
        st.markdown("""
        <div style="font-size:0.65rem;color:var(--text-muted);line-height:1.8;">
            <p><strong style="color:var(--accent);">📝 Blog Post</strong><br>Long-form articles with structured headings</p>
            <p><strong style="color:var(--accent);">💼 LinkedIn Post</strong><br>Professional social media content</p>
            <p><strong style="color:var(--accent);">📧 Email</strong><br>Professional email campaigns</p>
            <p><strong style="color:var(--accent);">📢 Ad Copy</strong><br>Conversion-focused advertisements</p>
            <p><strong style="color:var(--accent);">🏷️ Product Description</strong><br>Feature-focused product content</p>
            <p><strong style="color:var(--accent);">📱 Caption</strong><br>Social media captions with engagement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📄 Sample Outputs", expanded=False):
        st.markdown("""
        <div class="sample-box">
            <strong>📝 Blog:</strong> "10 AI Trends That Will Shape 2025" — 800 words
        </div>
        <div class="sample-box">
            <strong>💼 LinkedIn:</strong> "Excited to announce our new product! 🚀" — 150 words
        </div>
        <div class="sample-box">
            <strong>📧 Email:</strong> "Subject: Your 30% discount ends today!" — Professional
        </div>
        <div class="sample-box">
            <strong>📱 Caption:</strong> "Sunday vibes with our new collection! ✨" — 30 words
        </div>
        """, unsafe_allow_html=True)

# ================================================================
# 📝 MAIN CONTENT - COMPACT & CLEAN
# ================================================================
col1, col2 = st.columns([1, 1.2], gap="medium")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title"><span class="card-title-icon">✍️</span> Topic & Inputs</p>', unsafe_allow_html=True)
    
    topic = st.text_area(
        "",
        height=130,
        placeholder="Describe your topic in detail...\n\nExample: 'The future of artificial intelligence in healthcare'",
        label_visibility="collapsed"
    )
    
    keywords = st.text_input(
        "Keywords (Optional)",
        placeholder="e.g., AI, healthcare, innovation"
    )
    
    with st.expander("💡 Pro Tips", expanded=False):
        st.markdown("""
        <div style="font-size:0.7rem;color:var(--text-muted);line-height:1.8;">
            • <strong style="color:var(--accent);">Be specific</strong> about your topic<br>
            • <strong style="color:var(--accent);">Define your audience</strong> clearly<br>
            • <strong style="color:var(--accent);">Add keywords</strong> for SEO
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title"><span class="card-title-icon">📄</span> Generated Content</p>', unsafe_allow_html=True)
    
    # ============================================================
    # CLEAN OUTPUT - NO EXTRA SPACE
    # ============================================================
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    
    output_text = st.text_area(
        "",
        value=st.session_state.generated_content,
        height=260,
        key="output_editor",
        label_visibility="collapsed",
        placeholder="Your generated content will appear here..."
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================
    # PROFESSIONAL TOOLBAR BUTTONS
    # ============================================================
    st.markdown('<div class="toolbar">', unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5, gap="small")
    
    with col_btn1:
        st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
        if st.button("📋 Copy", use_container_width=True):
            st.toast("✅ Copied to clipboard!", icon="📋")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_btn2:
        st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
        if st.session_state.generated_content:
            st.download_button(
                label="📥 .txt",
                data=st.session_state.generated_content,
                file_name=f"genie_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_btn3:
        st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
        if st.session_state.generated_content:
            md_content = f"""# GenIE Content
**Template:** {template}
**Tone:** {tone}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---
{st.session_state.generated_content}

---
*Generated by GenIE - Enterprise AI Content Studio*
"""
            st.download_button(
                label="📝 .md",
                data=md_content,
                file_name=f"genie_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_btn4:
        st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.generated_content = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_btn5:
        st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
        if st.session_state.generated_content and output_format == "JSON Format":
            try:
                json_data = json.dumps({
                    "content": st.session_state.generated_content,
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
    prompt = get_template_prompt(template, topic, tone, length, audience, keywords, output_format)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert content writer with 10+ years of experience."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=800,
            top_p=0.9
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ================================================================
# 🧞 GENERATE LOGIC
# ================================================================
if generate_btn:
    if not topic:
        st.warning("⚠️ Please enter a topic before generating!")
    else:
        with st.spinner("◆ GenIE is generating your content..."):
            content = generate_content(template, tone, length, audience, topic, keywords, output_format)
            st.session_state.generated_content = content
            st.session_state.generation_count += 1
            st.rerun()

# ================================================================
# 📌 FOOTER
# ================================================================
st.markdown("""
<div class="footer">
    <p class="footer-text">
        <strong>◆ GenIE</strong> 
        <span class="footer-dot">•</span> 
        Enterprise AI Content Studio 
        <span class="footer-dot">•</span> 
        6 Templates • 8 Tones • 4 Formats
        <span class="footer-dot">•</span> 
        Innoviast Internship • Week 2
    </p>
</div>
""", unsafe_allow_html=True)