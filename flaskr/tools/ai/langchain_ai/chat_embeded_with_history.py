from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_chroma import Chroma
from langchain.schema import Document, HumanMessage, AIMessage
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

db_location = "./chrome_langchain_db"
embedding = FastEmbedEmbeddings()
collection_name = "alice_pdf"

# Loading vector store
vector_store = Chroma(persist_directory=db_location,
                          embedding_function=embedding, collection_name=collection_name)

# 2. Pull the standard RAG chat prompt
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# 3. Init Ollama LLM
llm = OllamaLLM(model="deepseek-coder-v2:16b") # bge-m3

# 4. Build the “combine docs” chain
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

# 5. Create the new retrieval chain
retrieval_chain = create_retrieval_chain(
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    combine_docs_chain=combine_docs_chain
)

# 6. Maintain and pass chat history on each turn
chat_history: list[HumanMessage | AIMessage] = []

def ask(question: str):
    print("User:", question)
    # Invoke with both the new input and the accumulated history
    result = retrieval_chain.invoke({
        "input": question,
        "chat_history": chat_history
    })
    answer = result["answer"]
    # Print and update history
    print("AI:", answer)
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

# Example conversation
ask("my name is yaniv")
ask("what is my name get it from chat history?")
# ask("who is Alice?")
# ask("What is the main idea of the book?")
