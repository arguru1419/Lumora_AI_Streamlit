# 🤖 Lumora AI – Enterprise AI Assistant

Lumora AI is a Streamlit-based Enterprise AI Assistant that enables users to chat with an AI model, upload documents, and ask context-aware questions using Retrieval-Augmented Generation (RAG). It provides a clean and intuitive interface for interacting with AI while leveraging uploaded documents for more accurate responses.

---

## 🚀 Features

- 💬 AI-powered conversational chat
- 📄 Upload PDF, DOCX, and TXT documents
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Context-aware question answering
- 📚 Multi-document support
- 💾 Chat history management
- 📤 Export chat as JSON
- 🆕 Multiple chat sessions
- 🎨 Clean and responsive Streamlit interface
- ⚡ Local LLM integration using Ollama

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI & NLP
- Ollama
- Local Large Language Model (LLM)
- Retrieval-Augmented Generation (RAG)

### Document Processing
- PyMuPDF
- python-docx

### Utilities
- JSON
- pathlib
- UUID

---

## 📂 Project Structure

```
Lumora-AI/
│
├── app.py
├── README.md
├── requirements.txt
│
├── core/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── prompt_builder.py
│   ├── guardrails.py
│   └── rate_limiter.py
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py
│   ├── rag_service.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── chat_history.py
│  
├── tools/
│   ├── __init__.py
│   ├── tool_registry.py
│   ├── summary_tool.py
│   └── statistics_tool.py
│
├── uploads/
├── chats/
├── assets/
└── logs/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/arguru1419/Lumora_AI_Streamlit.git
cd Lumora_AI_Streamlit
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

Download and install Ollama from:

https://ollama.com/

Pull the required model:

```bash
ollama pull qwen2.5:3b
```

Start Ollama:

```bash
ollama serve
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 📄 Supported Document Formats

- PDF
- DOCX
- TXT

---

## 💡 How to Use

1. Launch the application.
2. Upload one or more documents.
3. Wait for the documents to be indexed.
4. Ask questions about the uploaded documents.
5. Continue chatting with the AI assistant.
6. Export conversations if required.

---

## 📸 Screenshots

### Home Page

(Add screenshot here)

### Document Upload

(Add screenshot here)

### Chat Interface

(Add screenshot here)

---

## 🔮 Future Enhancements

- Voice Input
- Voice Output
- Authentication
- Database-backed chat history
- Vector database integration
- Cloud deployment
- Multi-user support
- Streaming AI responses

---

## 👨‍💻 Author

**Guru Prakash S**

- GitHub: https://github.com/arguru1419
- LinkedIn: *(Add your LinkedIn profile here)*

---

## 📄 License

This project is developed for educational purposes and technical assessment demonstrations.
