import os
import base64
from io import BytesIO
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage
from PIL import Image

model_name = "gemma3:4b" # "llava:7b"
current_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.abspath(current_path + "/../content/images/")
model = OllamaLLM(model=model_name, temperature=0.8)  #  phi4-mini:3.8b

def convert_to_base64(image_path: str) -> str:
    pil_image = Image.open(image_path)
    buffered = BytesIO()
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')  # Drop the alpha channel
    pil_image.save(buffered, format="JPEG")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# def convert_to_base64(image_path: str) -> str:
#     """
#     Opens an image file and converts it to a base64-encoded string.
#     """
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#     return encoded_string

chat_history = ""
while True:
    print("\n\n-------------------------------")
    pic_name = input("enter pic name or empty for chat only (q to quit): ")
    if pic_name == "q":
        break
    question = input("Ask your question (q to quit): ")
    if question == "q":
        break
    if pic_name == "": # "cow.jpg":
        llm_with_image_context = model
    else:
        image_url = os.path.abspath(f"{images_path}/{pic_name}")
        image_b64_pic1 = convert_to_base64(image_url)
        # can use multiple images
        llm_with_image_context = model.bind(images=[image_b64_pic1])
        if question == "":
            question = "What is in this picture?"  # answer in few sentences"
    print("")
    template = """
Here is the question to answer: {question}

Previous conversation: {chat_history}
"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm_with_image_context
    for chunk in chain.stream({"question": question, "chat_history": chat_history}):
        if chunk is not None:
            msg = chunk
            # chat_history += msg
            print(msg, end="")
    chat_history += question
