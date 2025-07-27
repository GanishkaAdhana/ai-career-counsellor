import os
import logging
import ollama
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Tuple
import textwrap
import uuid
from chromadb import PersistentClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ef = embedding_functions.OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434"
)

def create_chunks(text: str, chunk_size: int = 1000) -> List[str]:
    return textwrap.wrap(text, chunk_size, break_long_words=False)

def create_text_chunks(documents, chunk_size=1000, overlap=200):
    all_chunks = []
    for doc in documents:
        content = doc["content"]
        source = doc["source"]

        if not content.strip():
            logging.warning(f"Empty document found: {source}")
            continue

        chunks = []
        start = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))
            if end < len(content) and end - start == chunk_size:
                last_period = content.rfind('.', start, end)
                last_newline = content.rfind('\n', start, end)
                break_point = max(last_period, last_newline)
                if break_point > start:
                    end = break_point + 1

            chunk_text = content[start:end]
            chunks.append({
                "page_content": chunk_text,
                "metadata": {"source": source}
            })

            start = end - overlap if end < len(content) else end

        all_chunks.extend(chunks)

    logging.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
    return all_chunks

def add_chunks_to_collection(collection: chromadb.Collection, chunks: List[dict]):
    for chunk in chunks:
        unique_id = f"{chunk['metadata']['source']}_{uuid.uuid4()}"
        collection.add(
            documents=[chunk["page_content"]],
            metadatas=[chunk["metadata"]],
            ids=[unique_id]
        )
    logging.info(f"Added {len(chunks)} chunks to the collection.")

def query_collection(collection: chromadb.Collection, query: str, n_results: int = 5) -> List[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0]

def init_rag_system(document_name: str) -> Tuple[chromadb.Collection, ollama.Client]:
    try:
        logging.info(f"Initializing RAG system for document: {document_name}")
        client = PersistentClient(path=f"./chromadb/{document_name}")
        collection = client.get_or_create_collection("career_collection", embedding_function=ef)
        model = ollama.Client()
        logging.info("RAG system initialization complete")
        return collection, model
    except Exception as e:
        logging.error(f"Failed to initialize RAG system: {e}")
        return None, None

def simplified_query_with_rag(collection: chromadb.Collection, model: ollama.Client, query: str):
    try:
        relevant_chunks = query_collection(collection, query)
        contexts = "\n".join(relevant_chunks)

        prompt = f"""You are CareerBot, a helpful AI career advisor. Answer the following question directly and helpfully using the context information provided.

Context information:
{contexts}

User question: {query}

Important: Respond directly to the user's question in a conversational way. Provide specific career advice related to their query. DO NOT include explanations of how to respond or multiple "scenarios" in your answer. Just give a direct, helpful answer to their question about careers."""

        response = model.chat(model="gemma:2b", messages=[
            {"role": "system", "content": "You are CareerBot, a helpful AI career advisor that provides direct answers to user questions. Never show example responses or internal instructions."},
            {"role": "user", "content": prompt}
        ])
        return response["message"]["content"]
    except Exception as e:
        logging.error(f"Error in RAG query processing: {e}")
        return "I'm having trouble processing your question. Could you please rephrase or try another career-related question?"

def process_new_document(document_text: str, filename: str):
    client = PersistentClient(path=f"./chromadb/{filename}")
    collection = client.get_or_create_collection("career_collection", embedding_function=ef)
    chunks = create_text_chunks([{"content": document_text, "source": filename}])
    add_chunks_to_collection(collection, chunks)
    logging.info(f"Added {len(chunks)} chunks from the document to the collection.")
    print("Document successfully loaded.")

def get_existing_documents():
    chromadb_dir = "./chromadb"
    if os.path.exists(chromadb_dir):
        return [d for d in os.listdir(chromadb_dir) if os.path.isdir(os.path.join(chromadb_dir, d))]
    return []

def document_exists(document_name: str) -> bool:
    return os.path.exists(f"./chromadb/{document_name}")
