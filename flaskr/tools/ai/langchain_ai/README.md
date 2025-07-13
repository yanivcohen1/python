# RAG
Rag (Retreival Augmented Generation) Python solution with llama3, LangChain, Ollama and ChromaDB in a Flask API based solution

# install pip envirment
pip install pipenv
# for linux create virtual envirment
sudo apt install python3.8-venv

# create virtual envirment
py -3.12 -m venv venv
py -m venv venv
# in linux
python3 -m venv .venv

# ACTIVE IT
venv\Scripts\activate
# for linux
. .venv/bin/activate

# test it in cmd
where python
# in linux
which python3

# install pakeges in venv at editable mode (the source)
pip install -e .
# or install pakeges in venv at standart mode
python -m pip install .

# run the code
py exercise.py

# stop it
control + z

# save pakeges version
# create requirements.txt
pip freeze > requirements.txt
# install it
pip install -r requirements.txt

# disasmbly {app}.py
python -m dis {app}.py

# https://stackoverflow.com/questions/64742439/sphinx-cant-locate-conf-py-but-it-is-there
# run this command from docs folder to create html documentation in this folder
sphinx-build -E -b html -d build/doctrees source build/html


https://www.youtube.com/watch?v=7VAs22LC7WE
https://www.youtube.com/watch?v=E4l91XKQSgw

https://github.com/techwithtim/LocalAIAgentWithRAG/tree/main