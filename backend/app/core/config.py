from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = DATA_DIR / "index"
CONVERSATIONS_DIR = DATA_DIR / "conversations"

DATA_DIR.mkdir(exist_ok=True)
INDEX_DIR.mkdir(exist_ok=True)
CONVERSATIONS_DIR.mkdir(exist_ok=True)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 5
