import streamlit as st
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transcript_fetcher import get_video_id, get_transcript, format_transcript
from chunker import chunk_transcript
from embedder import embed_and_store
from rag import ask
from summarizer import summarize
from note_taking import take_notes

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AskTube",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

.stApp {
    background-color: #0d0d0d;
}

h1, h2, h3 {
    font-family: 'Space Mono', monospace;
}

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    color: #e8e8e8;
    letter-spacing: -2px;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #666;
    margin-bottom: 2.5rem;
    font-weight: 300;
}

.accent {
    color: #c8f135;
}

.status-box {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #c8f135;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #c8f135;
    margin-bottom: 1rem;
}

.result-box {
    background: #141414;
    border: 1px solid #222;
    padding: 1.25rem 1.5rem;
    border-radius: 6px;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #d4d4d4;
    margin-top: 1rem;
}

.timestamp-chip {
    display: inline-block;
    background: #1e1e1e;
    border: 1px solid #333;
    color: #c8f135;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 3px;
    margin: 2px;
    text-decoration: none;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

div[data-testid="stTextInput"] input {
    background: #141414 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 4px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 1rem !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #c8f135 !important;
    box-shadow: 0 0 0 1px #c8f135 !important;
}

div[data-testid="stSelectbox"] > div {
    background: #141414 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
}

.stButton > button {
    background: #c8f135 !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.15s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

.stButton > button:disabled {
    background: #2a2a2a !important;
    color: #555 !important;
}

div[data-testid="stRadio"] label {
    color: #aaa !important;
    font-size: 0.9rem !important;
}

div[data-testid="stRadio"] div[role="radio"][aria-checked="true"] + div {
    color: #c8f135 !important;
}

.stSpinner > div {
    border-top-color: #c8f135 !important;
}

hr {
    border-color: #1e1e1e !important;
}

.stTextArea textarea {
    background: #141414 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "video_ready" not in st.session_state:
    st.session_state.video_ready = False
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "summary" not in st.session_state:
    st.session_state.summary = None
if "notes" not in st.session_state:
    st.session_state.notes = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Ask<span class="accent">Tube</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Ask questions, summarize, and take notes from any YouTube video. Runs fully local.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Step 1: Video Input ───────────────────────────────────────────────────────
st.markdown('<div class="section-label">01 — Video</div>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
with col2:
    process_btn = st.button("PROCESS", disabled=not url)

if process_btn and url:
    with st.spinner("Fetching transcript and building knowledge base..."):
        try:
            video_id = get_video_id(url)
            transcript = get_transcript(video_id)
            format_transcript(transcript, video_id)
            chunk_transcript(video_id)
            embed_and_store(video_id)

            st.session_state.video_ready = True
            st.session_state.video_id = video_id
            st.session_state.chat_history = []
            st.session_state.summary = None
            st.session_state.notes = None

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

if st.session_state.video_ready:
    st.markdown(f'<div class="status-box">✓ VIDEO READY — {st.session_state.video_id}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Step 2: Mode ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">02 — Mode</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["ASK", "SUMMARIZE", "NOTES"])

    # ── Ask tab ───────────────────────────────────────────────────────────────
    with tab1:
        mode = st.radio(
            "",
            ["strict", "extended"],
            horizontal=True,
            label_visibility="collapsed",
            format_func=lambda x: f"{'🔒 Strict — video only' if x == 'strict' else '🌐 Extended — supplement with LLM knowledge'}"
        )

        q_col1, q_col2 = st.columns([5, 1])
        with q_col1:
            question = st.text_input("", placeholder="Ask anything about the video...", key="question_input", label_visibility="collapsed")
        with q_col2:
            ask_btn = st.button("ASK", disabled=not question)

        if ask_btn and question:
            with st.spinner("Searching and generating answer..."):
                try:
                    # Capture printed output
                    import io
                    from contextlib import redirect_stdout

                    f = io.StringIO()
                    with redirect_stdout(f):
                        response = ask(question, mode)

                    answer = response['message']['content']

                    # Get timestamp links from query
                    from query import query_chunks
                    chunks = query_chunks(question)
                    links = [m['timestamp_link'] for m in chunks['metadatas'][0]]
                    times = [f"{m['start_time']} – {m['end_time']}" for m in chunks['metadatas'][0]]

                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer,
                        "links": links,
                        "times": times
                    })

                except Exception as e:
                    st.error(f"Error: {str(e)}")

        # Chat history
        if st.session_state.chat_history:
            for item in reversed(st.session_state.chat_history):
                st.markdown(f"**Q: {item['question']}**")
                st.markdown(f'<div class="result-box">{item["answer"]}</div>', unsafe_allow_html=True)

                links_html = " ".join([
                    f'<a class="timestamp-chip" href="{link}" target="_blank">▶ {time}</a>'
                    for link, time in zip(item["links"], item["times"])
                ])
                st.markdown(f'<div style="margin-top:0.5rem">{links_html}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    # ── Summarize tab ─────────────────────────────────────────────────────────
    with tab2:
        if st.button("GENERATE SUMMARY"):
            with st.spinner("Summarizing video..."):
                try:
                    import io
                    from contextlib import redirect_stdout
                    f = io.StringIO()
                    with redirect_stdout(f):
                        response = summarize(st.session_state.video_id)
                    st.session_state.summary = response['message']['content']
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.session_state.summary:
            st.markdown(f'<div class="result-box">{st.session_state.summary}</div>', unsafe_allow_html=True)

    # ── Notes tab ─────────────────────────────────────────────────────────────
    with tab3:
        if st.button("GENERATE NOTES"):
            with st.spinner("Taking notes..."):
                try:
                    import io
                    from contextlib import redirect_stdout
                    f = io.StringIO()
                    with redirect_stdout(f):
                        response = take_notes(st.session_state.video_id)
                    st.session_state.notes = response['message']['content']
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.session_state.notes:
            st.markdown(f'<div class="result-box">{st.session_state.notes}</div>', unsafe_allow_html=True)