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


# read_root
@app.get("/")
def read_root():
    question = "请告诉我当前北京时间"
    # use python to print current time

    answer = question
    count = len(db.index())

    start_time = datetime.datetime.now()
    # answer = ai.run(question)
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    return {
        "duration": duration,
        "content": question,
        "Answer": answer,
        "count": count,
    }


# post_quest
@app.post("/api/quest")
def post_quest(hash: str, question: str, tasks: BackgroundTasks, token : str = None):
    # insert into db
    db.insert({
        "hash": hash,
        "question": question,
    })

    # background task to call ai
    tasks.add_task(post_ai_queue, hash, question, token)

    # I think domain is dynamic so I should not handle it
    BASE_URL = "http://192.168.3.95:8000"
    # BASE_URL = "http://ccmeta.cc:8000"

    url = BASE_URL + "/report?hash=" + hash
    return {"hash": hash, "question": question, "url": url}


# get_quest
@app.get("/api/quest")
def get_quest(hash: str):
    result = db.get(hash)
    return {"hash": hash, "result": result}


# post_ai_queue
def post_ai_queue(hash: str, question: str, token: str = None):
    answer = ai.run(question, token)
    print (answer)
    # update db with answer
    db.update(hash, answer.get("result"), answer.get("status"), answer.get("raw"))


# get_report
@app.get("/report")
def get_report(hash: str):
    return FileResponse("index.html")
