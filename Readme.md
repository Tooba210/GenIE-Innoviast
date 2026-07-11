# 🧞 GenIE — AI Content Studio

I built GenIE as a Streamlit web app that generates ready-to-use marketing and content copy — blog posts, LinkedIn posts, emails, ad copy, product descriptions, and captions — from a short topic description. It has a dark "ink & brass" scribe-studio theme and is powered by Groq's free, fast LLM API.

## Features

- **6 content types**: Blog Post, LinkedIn Post, Email, Ad Copy, Product Description, Caption
- **8 tones of voice**: Professional, Casual, Persuasive, Emotional, Humorous, Formal, Inspirational, Witty
- **3 length presets**: Short (50–80 words), Medium (150–250 words), Long (350–500 words)
- **4 output formats**: Paragraphs, Bullet Points, Numbered List, JSON
- **Editable output** — generated content appears in an editable text box, not a read-only preview
- **Export options**: copy to clipboard, download as `.txt`, download as `.md`, download as JSON
- **Optional keyword input** for SEO-oriented content
- **Target audience field** to tailor tone and framing
- **Generation counter** in the sidebar
- Clear error handling for rate limits and missing/invalid API keys (no raw stack traces shown to the user)

## Tech stack

| Layer | Choice |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| LLM provider | [Groq](https://console.groq.com) (free tier, no credit card) |
| Model | `llama-3.3-70b-versatile` |
| SDK | Official `groq` Python client |
| Config | `python-dotenv` (local) / Streamlit secrets (cloud) |

## Project structure

```
.
├── app.py              # Main Streamlit app (UI + generation logic)
├── requirements.txt    # Python dependencies
├── .env                # Local-only API key (not committed)
├── README.md
└── AI_usage.md          # Disclosure of AI assistance used on this project
```

## Setup (local)

1. **Clone the repo** and create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a free Groq API key** (no credit card required):
   👉 https://console.groq.com/keys

4. **Add your key to a `.env` file** in the project root:
   ```
   GROQ_API_KEY=your_key_here
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app pointing at `app.py`.
3. In **Settings → Secrets**, add your key at the **root level**:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. Reboot the app after adding/changing secrets — Streamlit Cloud doesn't hot-reload them.

## Usage

1. Pick a **Content Type**, **Tone**, **Length**, and (optionally) a **Target Audience** and **Keywords** in the sidebar.
2. Enter your topic in the left box.
3. Click **🧞 Generate Content**.
4. Edit the result directly in the right-hand box if needed, then copy or download it.

## Rate limits

The free Groq tier allows roughly 30 requests/minute and a daily request cap. If you hit the limit, GenIE shows a friendly message instead of crashing — just wait a minute and try again, or check your usage at `console.groq.com/settings/limits`.

## License

This project is for educational purposes as part of the Innoviast Internship Program.

## Acknowledgments
Innoviast — For the internship opportunity

Groq — For the free AI API

Streamlit — For the amazing UI framework

## Author
Tooba Rehman
AI Chatbot Developer Intern
Innoviast

🔗 GitHub: https://github.com/Tooba210/GenIE-Innoviast/blob/main/requirements.txt
🔗 Live Demo: https://genie-innoviast-g4mvd2ssiza7qzhqdiuv9l.streamlit.app/
🔗 LinkedIn: https://www.linkedin.com/in/tooba-rehman-ba99902a8/