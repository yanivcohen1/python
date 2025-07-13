from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from csv_vector import retriever

chat_model = ChatOpenAI(
        api_key="your_api_key_here",  # Replace with your actual API key
        temperature=0.8,
        model="deepseek-coder-v2:16b",  # or "gpt-3.5-turbo"
        base_url="http://localhost:11434/v1"
        # stream_usage=True,
        # callback_manager=callback_manager
)

template = """
You are an exeprt in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}

Previous conversation: {chat_history}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | chat_model

chat_history = ""
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n")
    if question == "q":
        break

    reviews = retriever.invoke(question)
    # result = chain.invoke({"reviews": reviews, "question": question})
    for chunk in chain.stream({"reviews": reviews, "question": question, "chat_history": chat_history}):
        # This will print each token as it is generated
        if chunk.content is not None:
            msg = chunk.content
            # chat_history += msg
            # Print the token without a newline
            print(msg, end="")
    chat_history += question
