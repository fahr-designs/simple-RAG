import os
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from config import DOCUMENTS_PATH, CHROMA_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents(path):
    """Load all .txt files from a directory."""
    documents = []
    for file_path in Path(path).glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append({
                'content': content,
                'source': str(file_path)
            })
    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks


def index_documents():
    """Load documents, chunk them, and store in ChromaDB."""
    print("Loading documents...")
    docs = load_documents(DOCUMENTS_PATH)
    
    if not docs:
        print(f"No .txt files found in {DOCUMENTS_PATH}")
        return
    
    print(f"Found {len(docs)} documents")
    
    # Initialize embedding model
    print("Loading embedding model...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("documents")
    except:
        pass
    
    collection = client.create_collection("documents")
    
    # Process each document
    all_chunks = []
    all_metadatas = []
    
    for doc in docs:
        chunks = chunk_text(doc['content'])
        print(f"  {doc['source']}: {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                'source': doc['source'],
                'chunk_id': i
            })
    
    print(f"\nGenerating embeddings for {len(all_chunks)} chunks...")
    embeddings = embedder.encode(all_chunks, show_progress_bar=True)
    
    print("Storing in ChromaDB...")
    collection.add(
        embeddings=embeddings.tolist(),
        documents=all_chunks,
        metadatas=all_metadatas,
        ids=[f"chunk_{i}" for i in range(len(all_chunks))]
    )
    
    print(f"✓ Indexed {len(all_chunks)} chunks from {len(docs)} documents")


if __name__ == "__main__":
    index_documents()