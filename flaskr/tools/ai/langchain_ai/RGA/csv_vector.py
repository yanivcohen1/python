import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(current_path + "/../content/docs/realistic_restaurant_reviews.csv")
df = df.dropna() # Remove missing values.
df = df.drop_duplicates() # Remove duplicates.
# df = df.reset_index(drop=True) # Reset index.
embeddings = OllamaEmbeddings(model="mxbai-embed-large:335m")

db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)
collection_name="restaurant_reviews"

vector_store = Chroma(persist_directory=db_location)
collections = vector_store._client.list_collections()
collection_exist = True if collection_name in collections else False

vector_store = Chroma(
    collection_name=collection_name,
    persist_directory=db_location,
    embedding_function=embeddings
)

if not collection_exist:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 20}
)
