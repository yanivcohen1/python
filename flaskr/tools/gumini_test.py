# https://ai.google.dev/tutorials/python_quickstart
import pathlib
import textwrap
import os
import configparser
import google.generativeai as genai

config = configparser.ConfigParser()
secsecss = config.read('flaskr/tools/env_local.ini')
# GEMINI_API_KEY = config['DEFAULT']['GEMINI_API_KEY']
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY is None:
    print("set GEMINI_API_KEY in environment variable")
    raise Exception("set GEMINI_API_KEY in environment variable")

# for jupiter
# from IPython.display import display
# from IPython.display import Markdown

# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=GEMINI_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("What is the meaning of life?")
# print(response.text)
# print(response.candidates)

while True:
    query = input("enter query:")
    response = model.generate_content(query)
    try: print(response.text)
    except Exception as e: pass
