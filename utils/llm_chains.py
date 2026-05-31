"""LLM chain utilities using OpenRouter for summaries, notes, MCQs, and Q&A."""

from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL, LLM_TEMPERATURE, MAX_TOKENS


def get_client():
    """Return an OpenAI client configured for OpenRouter."""
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )


def _call_llm(prompt: str) -> str:
    """Make a call to the LLM via OpenRouter."""
    client = get_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def generate_summary(text: str) -> str:
    """Generate a concise summary of the research paper."""
    prompt = f"""You are an expert research paper analyst. Provide a comprehensive yet concise 
summary of the following research paper content. Structure your summary with:

1. **Objective**: What is the main research question or goal?
2. **Methodology**: What approach or methods were used?
3. **Key Findings**: What are the main results?
4. **Contributions**: What are the novel contributions?
5. **Limitations**: Any noted limitations or future work?

Research Paper Content:
{text[:8000]}

Summary:"""
    return _call_llm(prompt)


def generate_notes(text: str) -> str:
    """Generate structured study notes from the paper."""
    prompt = f"""You are an expert academic note-taker. Create detailed, well-structured study 
notes from the following research paper content. Include:

- **Key Concepts & Definitions**
- **Important Equations/Formulas** (if any)
- **Main Arguments & Evidence**
- **Methodology Details**
- **Results & Implications**
- **Key Takeaways**

Use bullet points and clear formatting for easy review.

Research Paper Content:
{text[:8000]}

Study Notes:"""
    return _call_llm(prompt)


def generate_mcqs(text: str, num_questions: int = 5) -> str:
    """Generate multiple-choice questions from the paper."""
    prompt = f"""You are an expert educator. Generate {num_questions} multiple-choice questions 
(MCQs) based on the following research paper content. Each question should:

- Test understanding of key concepts
- Have 4 options (A, B, C, D)
- Include the correct answer with a brief explanation

Format each question as:
**Q[number]:** [Question]
- A) [Option]
- B) [Option]
- C) [Option]
- D) [Option]

**Answer:** [Letter] — [Brief explanation]

---

Research Paper Content:
{text[:8000]}

MCQs:"""
    return _call_llm(prompt)


def answer_question(context: str, question: str) -> str:
    """Answer a question using RAG context from the paper."""
    prompt = f"""You are a helpful research assistant. Answer the following question based 
strictly on the provided context from a research paper. If the answer cannot be found in the 
context, say "I couldn't find a direct answer to this in the paper."

Context from the paper:
{context}

Question: {question}

Answer:"""
    return _call_llm(prompt)
