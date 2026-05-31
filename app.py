"""AI Research Paper Assistant — Streamlit Application (Powered by OpenRouter)."""

import streamlit as st
from utils.pdf_processor import extract_text_from_pdf, get_text_chunks
from utils.vector_store import create_vector_store, similarity_search
from utils.llm_chains import (
    generate_summary,
    generate_notes,
    generate_mcqs,
    answer_question,
)
from config import OPENROUTER_API_KEY

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #5A6C7D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">📄 AI Research Paper Assistant</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Upload a research paper and generate summaries, notes, MCQs, or ask questions using RAG</p>',
    unsafe_allow_html=True,
)

# ─── API Key Check ──────────────────────────────────────────────────────────────
if not OPENROUTER_API_KEY:
    st.warning("⚠️ OpenRouter API key not found. Please set `OPENROUTER_API_KEY` in your `.env` file.")
    st.info("🔑 Get your free API key from [OpenRouter](https://openrouter.ai/keys)")
    api_key_input = st.text_input("Or enter your OpenRouter API key here:", type="password")
    if api_key_input:
        import os
        os.environ["OPENROUTER_API_KEY"] = api_key_input
        import config
        config.OPENROUTER_API_KEY = api_key_input
    else:
        st.stop()

# ─── Sidebar: PDF Upload ────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📁 Upload Paper")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a research paper in PDF format",
    )

    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** uploaded!")
        st.divider()
        st.markdown("### ⚙️ Settings")
        num_mcqs = st.slider("Number of MCQs", min_value=3, max_value=15, value=5)
    else:
        num_mcqs = 5

    st.divider()
    st.markdown(
        """
        ### 📖 How to Use
        1. Upload a research paper (PDF)
        2. Wait for processing
        3. Use the tabs to:
           - 📝 Get a summary
           - 📒 Generate study notes
           - ❓ Create MCQs
           - 💬 Ask questions (RAG)
        """
    )
    st.divider()
    st.caption("Powered by OpenRouter + Gemini 2.0 Flash ⚡")

# ─── Process PDF ────────────────────────────────────────────────────────────────
if uploaded_file:
    # Extract and cache text
    if "pdf_text" not in st.session_state or st.session_state.get("file_name") != uploaded_file.name:
        with st.spinner("📖 Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)
            if not text.strip():
                st.error("❌ Could not extract text from this PDF. It may be scanned/image-based.")
                st.stop()
            st.session_state.pdf_text = text
            st.session_state.file_name = uploaded_file.name

        with st.spinner("🔗 Processing document for search..."):
            chunks = get_text_chunks(text)
            vector_store = create_vector_store(chunks)
            st.session_state.vector_store = vector_store
            st.session_state.chunks = chunks

    # ─── Main Tabs ──────────────────────────────────────────────────────────────
    tab_summary, tab_notes, tab_mcqs, tab_qa = st.tabs(
        ["📝 Summary", "📒 Study Notes", "❓ MCQs", "💬 Ask Questions"]
    )

    # ── Summary Tab ─────────────────────────────────────────────────────────────
    with tab_summary:
        st.subheader("📝 Paper Summary")
        if st.button("Generate Summary", key="btn_summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                summary = generate_summary(st.session_state.pdf_text)
                st.session_state.summary = summary
        if "summary" in st.session_state:
            st.markdown(st.session_state.summary)

    # ── Notes Tab ───────────────────────────────────────────────────────────────
    with tab_notes:
        st.subheader("📒 Study Notes")
        if st.button("Generate Notes", key="btn_notes", use_container_width=True):
            with st.spinner("Generating study notes..."):
                notes = generate_notes(st.session_state.pdf_text)
                st.session_state.notes = notes
        if "notes" in st.session_state:
            st.markdown(st.session_state.notes)

    # ── MCQs Tab ────────────────────────────────────────────────────────────────
    with tab_mcqs:
        st.subheader("❓ Multiple Choice Questions")
        if st.button("Generate MCQs", key="btn_mcqs", use_container_width=True):
            with st.spinner(f"Generating {num_mcqs} MCQs..."):
                mcqs = generate_mcqs(st.session_state.pdf_text, num_questions=num_mcqs)
                st.session_state.mcqs = mcqs
        if "mcqs" in st.session_state:
            st.markdown(st.session_state.mcqs)

    # ── Q&A Tab (RAG) ──────────────────────────────────────────────────────────
    with tab_qa:
        st.subheader("💬 Ask Questions About the Paper")
        st.caption("Uses Retrieval-Augmented Generation (RAG) to find relevant context and answer.")

        # Chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User input
        user_question = st.chat_input("Ask a question about the paper...")
        if user_question:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                with st.spinner("Searching paper and generating answer..."):
                    relevant_chunks = similarity_search(
                        st.session_state.vector_store, user_question, k=4
                    )
                    context = "\n\n".join(relevant_chunks)
                    answer = answer_question(context, user_question)
                    st.markdown(answer)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )

else:
    # ─── Empty State ────────────────────────────────────────────────────────────
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            ### 📝 Summarize
            Get a structured summary covering objectives, methods, findings, and contributions.
            """
        )
    with col2:
        st.markdown(
            """
            ### 📒 Study Notes
            Auto-generate detailed notes with key concepts, formulas, and takeaways.
            """
        )
    with col3:
        st.markdown(
            """
            ### 💬 Ask Questions
            Chat with your paper using RAG-powered Q&A for precise answers.
            """
        )
