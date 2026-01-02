import chromadb
from sentence_transformers import SentenceTransformer
import requests
import json
from config import CHROMA_DB_PATH, OLLAMA_MODEL, TOP_K_RESULTS


def retrieve_context(query, top_k=TOP_K_RESULTS):
    """Retrieve relevant chunks for a query."""
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection("documents")
    
    query_embedding = embedder.encode([query])[0]
    
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    
    return results['documents'][0], results['metadatas'][0]


def generate_answer(query, context):
    """Generate answer using Ollama."""
    prompt = f"""Based on the following context, answer the question. If the answer isn't in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
    
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'stream': False
        }
    )
    
    return response.json()['response']


def ask(query):
    """Main query function."""
    print(f"\nQuestion: {query}\n")
    
    print("Retrieving relevant context...")
    contexts, metadatas = retrieve_context(query)
    
    print(f"Found {len(contexts)} relevant chunks\n")
    
    # Combine contexts
    combined_context = "\n\n".join(contexts)
    
    print("Generating answer...")
    answer = generate_answer(query, combined_context)
    
    print(f"\nAnswer: {answer}\n")
    
    print("Sources:")
    unique_sources = set(m['source'] for m in metadatas)
    for source in unique_sources:
        print(f"  - {source}")
    
    return answer


if __name__ == "__main__":
    # Interactive mode
    print(f"RAG System ready (using {OLLAMA_MODEL})")
    print("Type 'quit' to exit\n")
    
    while True:
        query = input("Ask a question: ").strip()
        if query.lower() in ['quit', 'exit', 'q']:
            break
        if query:
            ask(query)