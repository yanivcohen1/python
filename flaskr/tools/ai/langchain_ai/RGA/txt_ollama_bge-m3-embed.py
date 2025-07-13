import time
import ollama
import chromadb

# --- Configuration ---
OLLAMA_EMBED_MODEL = "bge-m3" # mxbai-embed-large:335m
OLLAMA_LLM = "deepseek-coder-v2:16b" # "llama3"  # Or mistral, phi3, etc. (make sure it's pulled)
CHROMA_PATH = "./chrome_langchain_db" # "./chroma_db" # Directory to store Chroma data
COLLECTION_NAME = "big_data_docs_bge"
TOP_K_RESULTS = 3 # How many relevant chunks to retrieve

# --- Sample Big Data Documents (Replace with your actual data loading) ---
# In a real scenario, you would load these from files, databases, etc.
# and split them into smaller, meaningful chunks.
documents = [
    "Big data refers to datasets that are too large or complex for traditional data-processing application software to adequately deal with.",
    "The characteristics of big data are often described by the 'Vs': Volume (large amounts of data), Velocity (high speed of data generation and processing), Variety (different types of data), Veracity (data uncertainty), and Value (extracting usefulness).",
    "Challenges in big data include storage, analysis, capture, data curation, search, sharing, transfer, visualization, querying, updating, information privacy, and data source.",
    "Big data processing often requires massively parallel software running on tens, hundreds, or even thousands of servers.",
    "Common big data technologies include distributed file systems like HDFS, databases like Cassandra and HBase, and processing frameworks like Apache Spark and Apache Flink.",
    "Data lakes are often used to store raw big data in various formats, while data warehouses store structured, processed data for analysis.",
    "Analyzing big data can uncover patterns, trends, and associations, especially relating to human behavior and interactions, leading to better business decisions.",
    "Privacy concerns are significant with big data, as aggregating diverse datasets can sometimes deanonymize individuals.",
    "Machine learning algorithms heavily rely on big data to train models effectively for tasks like prediction, classification, and clustering.",
    "The velocity aspect means data streams in continuously and needs to be processed in near real-time for applications like fraud detection or stock market analysis."
]

# --- ChromaDB Client Setup ---
# Use PersistentClient to save data to disk
client = chromadb.PersistentClient(path=CHROMA_PATH)

# --- Get or Create Chroma Collection ---
print(f"Getting or creating Chroma collection: {COLLECTION_NAME}")
try:
    collection = client.get_collection(name=COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' loaded.")
    # Optional: Clear the collection if you want to re-ingest
    # print("Clearing existing collection...")
    # client.delete_collection(name=COLLECTION_NAME)
    # collection = client.create_collection(name=COLLECTION_NAME)
    # print("Collection cleared and recreated.")

except Exception as e:
    print(f"Collection '{COLLECTION_NAME}' not found, creating...")
    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' created.")

# --- Ingestion Phase (Embed and Store) ---
if collection.count() < len(documents):
    print("\n--- Ingesting Documents ---")
    ids_to_add = []
    embeddings_to_add = []
    documents_to_add = []

    # Generate IDs that don't exist yet
    existing_ids = set(collection.get(include=[])['ids']) # Fetch existing IDs efficiently
    doc_id_counter = 0
    for i, doc in enumerate(documents):
        doc_id = f"doc_{i}"
        if doc_id not in existing_ids:
            print(f"Embedding document: {doc_id}")
            try:
                # Generate embedding using Ollama
                response = ollama.embeddings(model=OLLAMA_EMBED_MODEL, prompt=doc)
                ids_to_add.append(doc_id)
                embeddings_to_add.append(response["embedding"])
                documents_to_add.append(doc)
                # Small delay to avoid overwhelming the Ollama service if running locally
                time.sleep(0.1)
            except Exception as e:
                print(f"Error embedding document {doc_id}: {e}")

    if documents_to_add:
        print(f"\nAdding {len(documents_to_add)} new documents to Chroma...")
        collection.add(
            ids=ids_to_add,
            embeddings=embeddings_to_add,
            documents=documents_to_add
        )
        print("Ingestion complete.")
    else:
        print("No new documents to add.")
else:
    print("\n--- Documents already ingested ---")

print(f"Total documents in collection: {collection.count()}")

# --- Query Function ---
def query_rag(question: str) -> str:
    """
    Queries Chroma for relevant context and asks Ollama LLM for an answer.
    """
    print(f"\n--- Processing Query: '{question}' ---")

    # 1. Embed the question
    print("Embedding the question...")
    try:
        question_embedding = ollama.embeddings(
            prompt=question,
            model=OLLAMA_EMBED_MODEL
        )["embedding"]
    except Exception as e:
        return f"Error embedding question: {e}"

    # 2. Query Chroma for relevant documents
    print(f"Querying Chroma for top {TOP_K_RESULTS} relevant documents...")
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K_RESULTS,
        include=['documents'] # Only fetch the document text
    )

    retrieved_documents = results['documents'][0] # Get the list of documents for the first query

    if not retrieved_documents:
        print("No relevant documents found in Chroma.")
        # Optional: Fallback to asking LLM without context? Or return specific message.
        # For now, we'll try asking LLM without specific context
        context_str = "No specific context found."
    else:
        print("\nRetrieved Context:")
        for i, doc in enumerate(retrieved_documents):
            print(f"  {i+1}. {doc}")
        context_str = "\n".join(retrieved_documents)

    # 3. Construct the prompt for the LLM
    prompt_template = f"""Based ONLY on the following context, answer the question.
If the context does not contain the answer, state that the context is insufficient.

Context:
{context_str}

Question: {question}

Answer:"""

    print("\nSending prompt to Ollama LLM...")
    # print(f"--- Prompt --- \n{prompt_template}\n----------") # Uncomment to see the full prompt

    try:
        # 4. Send prompt to Ollama LLM
        response = ollama.chat(
            model=OLLAMA_LLM,
            messages=[{'role': 'user', 'content': prompt_template}]
        )
        final_answer = response['message']['content']
        print("\n--- Final Answer ---")
        return final_answer
    except Exception as e:
        return f"Error querying Ollama LLM: {e}"

# --- Example Usage ---
user_question = "What are the main challenges when dealing with big data?"
answer = query_rag(user_question)
print(answer)

print("-" * 30)

user_question_2 = "How does Apache Spark relate to big data?"
answer_2 = query_rag(user_question_2)
print(answer_2)

print("-" * 30)

user_question_3 = "What is the weather like today?" # Example of question likely not in context
answer_3 = query_rag(user_question_3)
print(answer_3)
