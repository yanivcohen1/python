from fastapi import FastAPI, Query
import uvicorn
# NLP Pkgs
from textblob import TextBlob

# Init App
app = FastAPI()

# Routes
@app.get('/')
async def index():
    return {'text': 'Hello FastAPI'}

@app.get('/sentiment/{text}')
async def get_sentiment(text):
    blob = TextBlob (text).sentiment
    results = {'original_text':text, 'polarity':blob.polarity, 'subjectivity':blob.subjectivity}
    return results


if __name__ == "__main__":
    uvicorn.run(app, port=8000) # host="0.0.0.0"
