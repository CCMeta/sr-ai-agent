import datetime
import ai
import db

from typing import Union
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


# app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# index_root
@app.get("/")
def index_root():
    return FileResponse("index.html")


# get_report
@app.get("/report")
def get_report(hash: str):
    return FileResponse("report.html")


# index_status
@app.get("/api/stats")
def index_status():
    return { "stats": db.count_all_status(), "code": 200 }


# index_quest
@app.get("/api/quest/index")
def index_quest():
    result = db.index()
    return { "topics": result, "code": 200 }


# get_quest
@app.get("/api/quest")
def get_quest(hash: str):
    result = db.get(hash)
    return {"hash": hash, "result": result}


# post_quest
@app.post("/api/quest")
def post_quest(hash: str, question: str, tasks: BackgroundTasks, token : str = None):
    # insert into db
    id = db.insert({
        "hash": hash,
        "question": question,
    })

    # background task to call ai
    tasks.add_task(post_ai_queue, id, question, token)

    # I think domain is dynamic so I should not handle it
    BASE_URL = "http://192.168.3.95:8000"
    # BASE_URL = "http://ccmeta.cc:8000"

    url = BASE_URL + "/report?hash=" + hash
    return {"hash": hash, "question": question, "url": url}


# post_ai_queue
def post_ai_queue(id: str, question: str, token: str = None):
    answer = ai.run(question, token)
    # update db with answer
    db.update(id, answer.get("result"), answer.get("status"), answer.get("raw"))
