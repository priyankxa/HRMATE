
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from llm import create_llm


# ==============================
# PATH CONFIGURATION
# ==============================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"

PDF_FILES = [
    ("handbook", "company_handbook.pdf", "policy"),
    ("job_description", "ai_developer_jd.pdf", "job_description"),
    ("resumes", "candidate_01.pdf", "resume"),
]


# ==============================
# LOAD AND PROCESS PDF FILES
# ==============================

def process_pdfs():
    documents = []

    for folder, filename, doc_type in PDF_FILES:
        file_path = DATA_DIR / folder / filename

        print(f"\nChecking PDF: {file_path}", flush=True)

        if not file_path.exists():
            print(f"PDF NOT FOUND: {file_path}", flush=True)
            continue

        try:
            loader = PyPDFLoader(str(file_path))
            pdf_docs = loader.load()

            for doc in pdf_docs:
                doc.metadata["document_type"] = doc_type
                doc.metadata["source_file"] = filename

            documents.extend(pdf_docs)

            print(
                f"Loaded {len(pdf_docs)} pages from {filename}",
                flush=True
            )

        except Exception as error:
            print(f"Error loading {filename}: {error}", flush=True)

    if not documents:
        print("\nNo PDF pages were loaded.", flush=True)
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # Remove chunks containing only whitespace.
    chunks = [
        chunk for chunk in chunks
        if chunk.page_content.strip()
    ]

    print(f"\nTotal PDF pages: {len(documents)}", flush=True)
    print(f"Total text chunks: {len(chunks)}", flush=True)

    return chunks


# ==============================
# INGEST PDF DATA INTO CHROMA
# ==============================

def ingest_data():
    print("\nStarting PDF ingestion...", flush=True)

    chunks = process_pdfs()

    if not chunks:
        print(
            "No text found. Check the PDF paths and PDF contents.",
            flush=True
        )
        return

    print("\nLoading embedding model...", flush=True)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    print("Connecting to Chroma database...", flush=True)

    vector_store = Chroma(
        collection_name="hr_documents",
        embedding_function=embeddings,
        persist_directory=str(DB_DIR)
    )

    print("Adding PDF chunks to database...", flush=True)

    try:
        # Avoid adding duplicate copies when ingestion is repeated.
        vector_store.reset_collection()
        vector_store.add_documents(chunks)

        count = vector_store._collection.count()

        print(
            f"\nIngestion successful! Stored chunks: {count}",
            flush=True
        )

    except Exception as error:
        print(f"\nIngestion failed: {error}", flush=True)
        raise


# ==============================
# ANSWER QUESTIONS USING RAG
# ==============================

def rag_chain(query):
    query = query.strip()

    if not query:
        return {"result": "Please enter a question."}

    try:
        print("\nStep 1: Loading embedding model...", flush=True)

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        print("Step 2: Connecting to Chroma...", flush=True)

        vector_store = Chroma(
            collection_name="hr_documents",
            embedding_function=embeddings,
            persist_directory=str(DB_DIR)
        )

        print("Step 3: Checking database...", flush=True)

        count = vector_store._collection.count()

        print(f"Stored chunks: {count}", flush=True)

        if count == 0:
            return {
                "result": (
                    "No PDF documents are stored yet. "
                    "Please run PDF ingestion first."
                )
            }

        print("Step 4: Searching relevant documents...", flush=True)

        docs = vector_store.similarity_search(query, k=3)

        if not docs:
            return {
                "result": "No relevant information found in the PDFs."
            }

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        print("Step 5: Loading Ollama LLM...", flush=True)

        llm = create_llm()

        prompt = f"""
You are HRMATE, an HR assistant.

Answer the user's question using only the provided company documents.
Give a clear and simple answer.
If the information is not available in the documents,
say that you could not find it in the provided documents.
Do not invent company policies or facts.

COMPANY DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

        print("Step 6: Generating answer...", flush=True)

        response = llm.invoke(prompt)

        answer = response.content

        print("Step 7: Answer generated successfully!", flush=True)

        return {"result": answer}

    except Exception as error:
        print(f"\nRAG ERROR: {error}", flush=True)

        return {
            "result": (
                f"Sorry, an error occurred while answering: {error}"
            )
        }


# ==============================
# RUN FROM TERMINAL
# ==============================

if __name__ == "__main__":
    print("\n========== HRMATE RAG SYSTEM ==========")
    print("1. Ingest PDF documents")
    print("2. Ask a question")
    print("3. Exit")

    choice = input("\nChoose (1, 2 or 3): ").strip()

    if choice == "1":
        ingest_data()

    elif choice == "2":
        question = input("\nEnter your question: ")
        result = rag_chain(question)

        print("\n========== ANSWER ==========")
        print(result["result"])

    elif choice == "3":
        print("Exiting HRMATE.")

    else:
        print("Invalid choice. Please select 1, 2 or 3.")
