import os
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformers
from config import DOCUMENTS_PATH, CHROMA_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP


"""Load all .txt files from specified directory."""
def load_all_documents(path):
    documents = []
    for file_path in Path(path).glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            documents.append({
                'content': content,
                'source': str(file_path)
            })
    return documents