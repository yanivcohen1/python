import os
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains.retrieval import create_retrieval_chain
# from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

db_location = "./chrome_langchain_db"

current_path = os.path.dirname(os.path.abspath(__file__))

docs_path = current_path + "/../content/docs/"

cached_llm = OllamaLLM(model="bge-m3") # mxbai-embed-large:335m

embedding = FastEmbedEmbeddings()

collection_name = "alice_pdf"

text_splitter = RecursiveCharacterTextSplitter( # 80 characters overlap between chunks (for not cut sentences)
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

collection_name="restaurant_reviews"

def ask_ai(query: str):

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer


def ask_PDF(file_name: str, chanks_size: int = 20):
    collection_name = file_name.replace(".", "_")

    # Loading vector store
    vector_store = Chroma(persist_directory=db_location,
                          embedding_function=embedding, collection_name=collection_name)

    chanks_len = get_chanks_len(collection_name)
    chanks_seg = chanks_size if chanks_len > chanks_size else chanks_len
    print(f"chanks_seg: {chanks_seg}")
    retriever = vector_store.as_retriever(
        search_kwargs={"k": chanks_seg} # 10% of chanks
    )

    return retriever


def pdf_to_vector(file_name: str):
    save_file = docs_path + file_name
    print(f"filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    chunks = loader.load_and_split(text_splitter=text_splitter)
    print(f"docs len={len(chunks)}")
    collection_name = file_name.replace(".", "_")

    collections = get_collection_names()
    collection_exist = True if collection_name in collections else False

    if collection_exist:
        print(f"collection {collection_name} already exist")
        del_collection(collection_name)

    # save chunks(docs) to collection_name
    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding,
        persist_directory=db_location, collection_name=collection_name
    )

    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "chunks": len(chunks),
    }
    print(f"response: {response}")
    return response


def get_collection_names():
    vector_store = Chroma(persist_directory=db_location) # , embedding_function=embedding
    collections = vector_store._client.list_collections()
    print(f"collections: {collections}")
    return collections

def del_collection(collection_name: str):
    vector_store = Chroma(persist_directory=db_location) # , embedding_function=embedding
    vector_store._client.delete_collection(collection_name)
    print(f"deleted collection: {collection_name}")
    return True

def get_chanks_len(collection_name: str):
    vector_store = Chroma(persist_directory=db_location, embedding_function=embedding, collection_name=collection_name)
    collection = vector_store._client.get_collection(collection_name)
    all_ids = collection.get()
    num_docs = len(all_ids["ids"])
    print(f"num_docs(chanks): {num_docs}")
    return num_docs

if __name__ == "__main__":
    # get_collection_names()
    # get_chanks_len("alice_pdf") # 573
    # del_collection("alice_pdf")
    # pdf_to_vector("alice.pdf")
    get_collection_names()
