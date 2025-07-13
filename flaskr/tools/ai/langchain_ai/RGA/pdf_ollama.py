from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pdf_vector import ask_PDF

model = OllamaLLM(model="deepseek-coder-v2:16b", temperature=0.8) # gemma3:4b phi4-mini:3.8b

pdf ="alice.pdf"

template = """
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
        question = "who is Alice? answer in few sentences"
    if question == "q":
        break
    # for attation and nlp for search (not just similarity search)
    reviews = ask_PDF(pdf).invoke(question) # returtn 60 chanks is 10% of chanks, 8 pages of 80 pages
    # result = chain.invoke({"reviews": reviews, "question": question})
    print("")
    for chunk in chain.stream({"reviews": reviews, "question": question, "chat_history": chat_history}):
        if chunk is not None:
            msg = chunk
            # chat_history += msg
            print(msg, end="")
    chat_history += question
