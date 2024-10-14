import json
import os
from os import listdir
from os.path import isfile

import spacy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from Classes import Ranker

app = FastAPI()


origins = [
"*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Allow specified origins
    allow_credentials=True,      # Allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],        # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],        # Allow all headers
)

nlp = spacy.load("hu_core_news_lg")
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

searchEngine = Ranker(config["database"] + ".index")
@app.get("/")
async def root():
    return FileResponse(config["root"]+"index.html")

@app.get("/database")
async def database():
    print("ez egy test")
    path = config["database"]
    files = [f for f in listdir(path) if isfile(path + f)]
    print(files)
    return files

@app.get("/database/{file}")
async def database_file(file: str):
    if not os.path.exists(config["database"] + file):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(config["database"] + file)

@app.get("/{file}")
async def get_file(file: str):
    if isfile(config["root"] + file):
        return FileResponse(config["root"] + file)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404 :
        return FileResponse(config["root"]+"404.html")

@app.get("/search/{tokens}")
def search(tokens: str):
    print(tokens)
    doc = nlp(tokens)
    return list(searchEngine.lookup(doc))