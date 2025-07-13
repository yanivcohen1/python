from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from csv_vector import retriever

model = OllamaLLM(model="deepseek-coder-v2:16b", temperature=0.8) # gemma3:4b phi4-mini:3.8b

template = """
You are an exeprt in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}

Previous conversation: {chat_history}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

chat_history = ""
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    if question == "":
        question = "what is the pizza quality?  answer in few sentences"
    print("\n")
    if question == "q":
        break

    # for attation and nlp for search
    reviews = retriever.invoke(question) # return 5 reviews
    # result = chain.invoke({"reviews": reviews, "question": question})
    for chunk in chain.stream({"reviews": reviews, "question": question, "chat_history": chat_history}):
        if chunk is not None:
            msg = chunk
            # chat_history += msg
            print(msg, end="")
    chat_history += question
