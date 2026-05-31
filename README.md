# 📄 AI Research Paper Assistant

An intelligent Streamlit application that helps you analyze research papers using AI. Upload any PDF and instantly generate summaries, study notes, MCQs, and ask questions using RAG (Retrieval-Augmented Generation).

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37-red.svg)
![AI](https://img.shields.io/badge/AI-OrcaRouter-orange.svg)

## 🌐 Live Demo

[**Try it here →**](https://ai-research-paper-assistant.streamlit.app)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Summary** | Structured summary with objectives, methodology, findings, contributions & limitations |
| 📒 **Study Notes** | Detailed notes with key concepts, formulas, arguments & takeaways |
| ❓ **MCQs** | Auto-generated multiple choice questions with answers & explanations |
| 💬 **Q&A (RAG)** | Chat with your paper — ask questions and get precise, context-aware answers |

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  PDF Upload │────▶│ Text Extract │────▶│  Text Chunking  │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                                    ┌──────────────▼──────────────┐
                                    │   TF-IDF Vector Store        │
                                    │   (Local - No API needed)    │
                                    └──────────────┬──────────────┘
                                                   │
                         ┌─────────────────────────▼─────────────────────────┐
                         │              OrcaRouter AI (Auto Model)            │
                         │  (Summary / Notes / MCQs / RAG Q&A)               │
                         └───────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
AI Research Paper Assistant/
├── app.py                  # Main Streamlit application
├── config.py               # Configuration & environment variables
├── requirements.txt        # Python dependencies
├── .env                    # Your API key (not committed)
├── .env.example            # Example env file
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── utils/
    ├── __init__.py
    ├── pdf_processor.py    # PDF text extraction & chunking
    ├── vector_store.py     # TF-IDF vector store & similarity search
    └── llm_chains.py       # LLM calls via OrcaRouter
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9 or higher
- OrcaRouter API key

### Step 1: Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-research-paper-assistant.git
cd ai-research-paper-assistant
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API key
Create a `.env` file:
```
OPENROUTER_API_KEY=your-orcarouter-api-key-here
```

### Step 4: Run the app
```bash
streamlit run app.py
```

## ☁️ Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `OPENROUTER_API_KEY` in Streamlit secrets
5. Deploy!

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: OrcaRouter (Auto model selection)
- **Embeddings**: TF-IDF (scikit-learn, local)
- **PDF Processing**: PyPDF2
- **Language**: Python

## 📄 License

MIT License — free to use and modify.
