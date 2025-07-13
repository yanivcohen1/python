import os
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains.retrieval import create_retrieval_chain
# from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

folder_path = "./chrome_langchain_db"

current_path = os.path.dirname(os.path.abspath(__file__))

docs_path = current_path + "/../content/docs/"

cached_llm = OllamaLLM(model="mxbai-embed-large:335m")

embedding = FastEmbedEmbeddings()

collection_name = "alice_pdf"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=384, chunk_overlap=80, length_function=len, is_separator_regex=False
)

def get_collection_names():
    vector_store = Chroma(persist_directory=folder_path) # , embedding_function=embedding
    collections = vector_store._client.list_collections()
    print(f"collections: {collections}")
    return collections

def del_collection(collection_name: str):
    vector_store = Chroma(persist_directory=folder_path) # , embedding_function=embedding
    vector_store._client.delete_collection(collection_name)
    print(f"deleted collection: {collection_name}")
    return True

def get_chanks_len(collection_name: str):
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding, collection_name=collection_name)
    collection = vector_store._client.get_collection(collection_name)
    result = collection.get() # limit=1, offset=0)
    doc_size = len(result["documents"][0])
    num_docs = len(result["ids"])
    print(f"single chank(doc) size: {doc_size}")
    print(f"number of docs(chanks): {num_docs}")

def is_collection_exist(collection_name: str) -> bool:
    vector_store = Chroma(persist_directory=folder_path)
    try:
        collection = vector_store._client.get_collection(collection_name)
        print(f"Collection '{collection_name}' found.")
        return True
    except Exception as e:
        print(f"Collection '{collection_name}' not found.")
        return False
if __name__ == "__main__":
    is_collection_exist("alice_pdf")
    # get_collection_names()
    # get_chanks_len("alice_pdf") # 573 * 386
    # get_chanks_len("pdf") # 205 * 1024
    # get_chanks_len("restaurant_reviews") # 123 * 386
    # del_collection("big_data_docs_bge_m3_1")
    # pdf_to_vector("alice.pdf")
    # get_collection_names()
