# Healix AI — Clinical AI Diagnostic Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/LLM-Groq%20LLaMA--3.3--70b--versatile-00c853.svg)](https://groq.com/)
[![VectorDB](https://img.shields.io/badge/VectorDB-Pinecone-0066cc.svg)](https://www.pinecone.io/)
[![Framework](https://img.shields.io/badge/Backend-Flask%20%2B%20LangChain-black.svg)](https://flask.palletsprojects.com/)
[![Styling](https://img.shields.io/badge/Styling-Tailwind%20CSS%20(Dark%20Mode)-18181b.svg)](https://tailwindcss.com/)

**Healix AI** is a state-of-the-art, privacy-preserving clinical diagnostic assistant. Built with a high-performance Retrieval-Augmented Generation (RAG) pipeline, Healix AI couples the **Groq LLaMA 3.3-70b-versatile** model with a **Pinecone vector index** to deliver grounded, evidence-based medical information while maintaining a completely **stateless server architecture**.

---

## ⚡ Key Highlights & Architecture

```
   +--------------------------------------------------------------+
   |                     Browser Client (Healix AI)              |
   |  - HTML5 LocalStorage Consultation Vault                    |
   |  - True-Neutral Dark Theme (Zinc-950 / Tech Green)          |
   |  - Responsive Collapsible Drawer & Triage Suggestion Chips   |
   +------------------------------+-------------------------------+
                                  |
               POST /get (JSON: { msg, history })
                                  |
                                  v
   +--------------------------------------------------------------+
   |                      Stateless Flask API                     |
   |  - Zero Server-Side DB / Memory Leaks                        |
   |  - Dynamic LangChain MessagesPlaceholder Injection           |
   +--------------+-------------------------------+---------------+
                  |                               |
        Similarity Query                  Prompt Assembly
                  v                               v
   +-------------------------------+   +--------------------------+
   |        Pinecone Index         |   |       Groq Cloud         |
   |  - HuggingFace 384-d Embeds   |   |  LLaMA 3.3-70b-versatile |
   |  - Validated Medical Book RAG |   |  Contextual Clinical Q&A |
   +-------------------------------+   +--------------------------+
```

- **Stateless Backend Design**: The Flask backend operates without local session storage or SQLite databases. Recent conversation turns are transferred directly within client payloads and mapped to LangChain `HumanMessage` and `AIMessage` objects on the fly.
- **Client-Side Local Vault**: All past consultations, UUIDs, timestamps, and message histories reside securely within the user's browser `localStorage`.
- **True Black & Tech Green Medical Aesthetics**: Implemented with Tailwind CSS, featuring deep `zinc-950` backdrops, elevated `zinc-900` cards, floating pill input consoles, and vibrant medical green accents.
- **Strict Startup Homepage**: Clean initial page load displaying the "Welcome to Healix AI" empty-state screen with interactive clinical suggestion chips (Cold vs. Flu, Hypertension, Vaccine Schedules, Migraines).
- **Lazy Session Initialization**: Consultation sessions and sidebar items are instantiated dynamically only upon the user's first query submission.

---

## 📁 Repository Structure

```text
.
├── .dockerignore              # Prevents sensitive files & data from leaking into Docker
├── .env.example               # Environment variables template
├── .gitignore                 # Comprehensive Git exclusion rules
├── Dockerfile                 # Containerization build recipe
├── README.md                  # Project overview and deployment guide
├── app.py                     # Stateless Flask API & LangChain RAG pipeline
├── requirements.txt           # Python package dependencies
├── setup.py                   # Package setup configuration
├── store_index.py             # Script to extract, embed, and upsert medical docs
├── data/
│   └── Medical_book.pdf       # Source clinical reference literature
├── research/
│   └── trials.ipynb           # RAG and LLM experimentation notebook
├── src/
│   ├── __init__.py
│   ├── helper.py              # PDF chunking and embedding utilities
│   └── prompt.py              # System prompt and clinical instructions
├── static/
│   └── style.css              # Legacy baseline styling
└── templates/
    └── chat.html              # Healix AI true-black clinical interface
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Nijjil-Narula/Healix-AI.git
cd Healix-AI
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Populate `.env` with your API keys:

```ini
PINECONE_API_KEY="your-pinecone-api-key"
GROQ_API_KEY="your-groq-api-key"
```

### 5. Ingest Knowledge Base into Pinecone (One-Time Setup)

```bash
python store_index.py
```

### 6. Launch the Application

```bash
python app.py
```

Access the application in your browser at `http://localhost:8080`.

---

## 🐳 Docker Deployment

Build the container image:

```bash
docker build -t healix-ai .
```

Run the container:

```bash
docker run -p 8080:8080 --env-file .env healix-ai
```

---

## 🔒 Security & Privacy

- **Zero DB Persistence**: Conversations are not retained in server databases or server-side logs.
- **Restricted Container Build**: Sensitive keys (`.env`), raw data files (`data/`), and internal notebooks (`research/`) are explicitly excluded via `.dockerignore`.
- **Disclaimer**: *Healix AI provides clinical information for reference and educational triage only. In acute medical emergencies, immediately contact local emergency services.*

---

## 👨‍💻 Author

**Nijjil Narula**
- GitHub: [@Nijjil-Narula](https://github.com/Nijjil-Narula)
