import os
from flask import Flask, request
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
# from langchain_community.vectorstores import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = Flask(__name__)

folder_path = "./chrome_langchain_db"

current_path = os.path.dirname(os.path.abspath(__file__))

docs_path = current_path + "/../content/docs/"

cached_llm = OllamaLLM(model="llama3:8b")

embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """
    <s>[INST] You are a technical assistant good at searching docuemnts. If you do not have an answer from the provided information say so. [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)


@app.route("/ai", methods=["POST"])
def aiPost():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer


@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    print("Post /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding, collection_name="pdf")

    print("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)

    sources = []
    for doc in result["context"]:
        sources.append(
            {"source": doc.metadata["source"], "page_content": doc.page_content}
        )

    response_answer = {"answer": result["answer"], "sources": sources}
    return response_answer


@app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    file_name = file.filename

    save_file = docs_path + file_name
    file.save(save_file)
    print(f"filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path, collection_name="pdf"
    )

    # vector_store.persist()

    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return response


# in production, use a WSGI server like Gunicorn or uWSGI to serve the Flask app.
# gunicorn -w 4 -b 0.0.0.0:8000 app:app
def start_app():
    app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    start_app()

# Example usage:
# 1. Use curl or Postman to send a POST request to the /ai endpoint with a query.
# curl -X POST -H "Content-Type: application/json" -d '{"query": "What is france capital?"}' http://localhost:8000/ai
# 2. Use curl or Postman to send a POST request to the /pdf endpoint with a PDF file.
# curl -X POST -F "file=@./alice.pdf" http://localhost:8000/pdf
# 3. Use curl or Postman to send a POST request to the /ask_pdf endpoint with a query.
# curl -X POST -H "Content-Type: application/json" -d '{"query": "who is Alice?"}' http://localhost:8000/ask_pdf
