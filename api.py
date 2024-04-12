from fastapi import FastAPI
import completion
from scrabNews import scrabNews
from dbConnect import dbConnect

app = FastAPI()

@app.get("/")
async def read_root():
    return "This is root path from MyAPI"

@app.post("/checkIntent")
async def checkIntent(prompt: str):
    return {"response": completion.ask_openai_gpt(prompt)}

@app.post("/getNewsList")
async def getNewList(keyword: str):
    return scrabNews(keyword)

@app.post("/ra")
async def rag(prompt: str):
    db_connector = dbConnect()
    return {"response": db_connector.retrivalAugment(prompt)}

@app.post("/generate")
async def generate(prompt: str):
    db_connector = dbConnect()
    doc = db_connector.retrivalAugment(prompt)
    prompt = 'Please create an answer for [question]. please answer with external knowledge. Please do not specify the source of the data in the answer. Please do not answer in short answer. \n [question]\n'+ prompt + '\n'+ doc
    return {"response": completion.ask_openai_gpt(prompt)}