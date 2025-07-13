import os
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Configuration ---
OLLAMA_EMBED_MODEL = "bge-m3"
OLLAMA_LLM = "deepseek-coder-v2:16b"
CHROMA_PATH = "./chrome_langchain_db" # Use a different path for clarity
COLLECTION_NAME = "big_data_docs_bge_m3" # Name of the collection in Chroma
TOP_K_RESULTS = 3 # How many relevant chunks to retrieve

# --- Sample Big Data Documents (Source Data) ---
# In a real scenario, you would use LangChain's Document Loaders
# (e.g., PyPDFLoader, WebBaseLoader, TextLoader)
documents_text = [
    "Big data refers to datasets that are too large or complex for traditional data-processing application software to adequately deal with. Data with many fields (columns) offer greater statistical power, while data with higher complexity (more attributes or columns) may lead to a higher false discovery rate.",
    "The characteristics of big data are often described by the 'Vs': Volume (large amounts of data), Velocity (high speed of data generation and processing), Variety (different types of data from various sources like text, images, videos), Veracity (data uncertainty, trustworthiness, and quality), and Value (extracting usefulness and insights). Some sources also add Variability (changes in data flow rates) and Complexity.",
    "Major challenges in big data include storage infrastructure costs, scalability, data analysis capabilities, capture methods, data curation standards, efficient search mechanisms, sharing policies, secure transfer methods, effective visualization techniques, querying large datasets, timely updates, information privacy regulations, and validating data sources.",
    "Processing big data typically requires massively parallel processing (MPP) databases, distributed file systems, and parallel software frameworks running on tens, hundreds, or even thousands of commodity servers. This horizontal scaling approach contrasts with traditional vertical scaling.",
    "Common technologies in the big data ecosystem include distributed file systems like Hadoop Distributed File System (HDFS), NoSQL databases such as Apache Cassandra, MongoDB, and HBase, stream processing tools like Kafka and Storm, and large-scale data processing frameworks like Apache Spark and Apache Flink. Cloud platforms also offer managed big data services.",
    "Data lakes are storage repositories that hold vast amounts of raw data in its native format until it's needed. They contrast with data warehouses, which typically store structured, filtered data that has already been processed for a specific purpose. Data lakes offer flexibility but require robust data governance.",
    "Analyzing big data sets allows analysts, researchers, and business users to make better and faster decisions using data that was previously inaccessible or unusable. Businesses can use insights to gain competitive advantages, target customers more effectively, and optimize operations. Machine learning heavily relies on big data.",
    "Significant privacy concerns arise with big data collection and analysis. Aggregating anonymized datasets can potentially re-identify individuals (data linkage). Ethical considerations and regulations like GDPR and CCPA are crucial for responsible big data practices.",
    "Machine learning algorithms, particularly deep learning, require vast amounts of training data (often big data) to build accurate models for tasks like image recognition, natural language processing, prediction, classification, anomaly detection, and recommendation systems.",
    "The velocity dimension of big data refers to the speed at which data is generated and must be processed. Real-time or near real-time processing is essential for applications like high-frequency trading, IoT sensor monitoring, fraud detection, and real-time bidding in online advertising."
]

# Wrap the raw text in LangChain Document objects
# Include metadata if available (e.g., source file name)
documents = [Document(page_content=text, metadata={"source": f"doc_{i}"}) for i, text in enumerate(documents_text)]

# --- Text Splitting ---
print("--- Splitting Documents ---")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,  # Adjust chunk size as needed
    chunk_overlap=80   # Adjust overlap as needed
)
chunks = text_splitter.split_documents(documents)
print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
# print(f"Example chunk:\n{chunks[0].page_content}\nMetadata: {chunks[0].metadata}") # Uncomment to see an example chunk

# --- Initialize Ollama Embeddings ---
# Use Ollama to generate embeddings client-side
print(f"--- Initializing Ollama Embeddings ({OLLAMA_EMBED_MODEL}) ---")
embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)

# --- Setup Chroma Vector Store ---
print(f"--- Setting up Chroma Vector Store (Collection: {COLLECTION_NAME}) ---")
# Check if the database directory exists to decide whether to load or create
vector_store = Chroma(persist_directory=CHROMA_PATH)
try:
    collection = vector_store._client.get_collection(COLLECTION_NAME)
    exist_collection = True
except Exception as e:
    exist_collection = False

if exist_collection:
    print(f"Loading existing Chroma database from: {CHROMA_PATH}")
    vectorstore = Chroma(
      persist_directory=CHROMA_PATH,
      embedding_function=embeddings,
      collection_name=COLLECTION_NAME
    )
    # Optional: Add new chunks if needed (more complex logic required to check for existing content)
    # current_doc_count = vectorstore._collection.count() # Access Chroma client directly if needed
    # print(f"Existing documents in collection: {current_doc_count}")
    # # Potentially compare `chunks` with existing docs and use vectorstore.add_documents()
else:
    print(f"Creating new Chroma database at: {CHROMA_PATH}")
    vectorstore = Chroma.from_documents(
        documents=chunks,                 # Add the split chunks
        embedding=embeddings,             # Use the Ollama embeddings
        persist_directory=CHROMA_PATH,    # Directory to save the database
        collection_name=COLLECTION_NAME   # Name of the collection
    )
    print("Database created and documents embedded.")

print(f"Vector store initialized. Total documents in collection: {vectorstore._collection.count()}")


# --- Initialize Ollama LLM ---
print(f"--- Initializing Ollama LLM ({OLLAMA_LLM}) ---")
llm = OllamaLLM(model=OLLAMA_LLM, temperature=0) # Use low temperature for factual answers

# --- Create Retriever ---
print(f"--- Creating Retriever (Top K: {TOP_K_RESULTS}) ---")
retriever = vectorstore.as_retriever(
    search_type="similarity", # Or "mmr"
    search_kwargs={"k": TOP_K_RESULTS} # Retrieve top K results
)

# --- Define Prompt Template ---
# RAG prompt template instructs the LLM how to use the retrieved context
template = """Answer the question based ONLY on the following context.
If the context does not contain the answer, state clearly that the answer is not found in the provided context.

Context:
{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# --- Helper Function to Format Retrieved Documents ---
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- Build RAG Chain using LangChain Expression Language (LCEL) ---
print("--- Building RAG Chain ---")
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()} # Pass question through, format retrieved docs
    | prompt                                                              # Pipe context and question to prompt
    | llm                                                                 # Pipe prompt to LLM
    | StrOutputParser()                                                   # Parse LLM output as string
)

# --- Query Function ---
def query_langchain_rag(question: str):
    """
    Queries the LangChain RAG pipeline.
    """
    print(f"\n--- Processing Query using LangChain RAG: '{question}' ---")
    try:
        start_time = time.time()
        answer = rag_chain.invoke(question)
        end_time = time.time()
        print(f"Query processed in {end_time - start_time:.2f} seconds.")
        print("\n--- Final Answer (LangChain RAG) ---")
        return answer
    except Exception as e:
        return f"Error processing RAG chain: {e}"

# --- Example Usage ---
import time # Add import for timing

user_question = "What are the main challenges when dealing with big data?"
answer = query_langchain_rag(user_question)
print(answer)

print("-" * 30)

user_question_2 = "How does Apache Spark relate to big data?"
answer_2 = query_langchain_rag(user_question_2)
print(answer_2)

print("-" * 30)

user_question_3 = "What is the weather today?" # Example of question likely not in context
answer_3 = query_langchain_rag(user_question_3)
print(answer_3)
