
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
CHAT_FOLDER = BASE_DIR / "chats"
LOG_FOLDER = BASE_DIR / "logs"

UPLOAD_FOLDER.mkdir(exist_ok=True)
CHAT_FOLDER.mkdir(exist_ok=True)
LOG_FOLDER.mkdir(exist_ok=True)

# --------------------------------------------------
# LLM
# --------------------------------------------------

MODEL_NAME = "qwen2.5:3b"
TEMPERATURE = 0.3
MAX_TOKENS = 512
OLLAMA_HOST = "http://localhost:11434"

SYSTEM_PROMPT = (
    "You are Lumora AI, an enterprise AI assistant. "
    "Answer clearly, professionally, and use uploaded "
    "documents whenever possible. If the answer is not "
    "available in the document, say so instead of guessing."
)

# --------------------------------------------------
# RAG
# --------------------------------------------------

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 3

# --------------------------------------------------
# Rate Limiting
# --------------------------------------------------

MAX_REQUESTS = 5
RATE_LIMIT_WINDOW = 60

# --------------------------------------------------
# UI
# --------------------------------------------------

APP_TITLE = "Lumora AI"
APP_ICON = "🤖"