import datetime
import ai
import db

from typing import Union
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.post("/api/quest")
def post_quest(hash: str, question: str, tasks: BackgroundTasks):
    # insert into db
    db.insert({
        "hash": hash,
        "question": question,
    })

    # background task to call ai
    tasks.add_task(post_ai_queue, hash, question)

    url = "http://ccmeta.cc:8000/report/" + hash
    return {"hash": hash, "question": question, "url": url}

@app.get("/api/quest/{hash}")
def get_quest(hash: str):
    result = db.get(hash)
    return {"hash": hash, "result": result}

def post_ai_queue(hash: str, question: str):
    answer = ai.run(question)
    # update db with answer
    db.update(hash, answer)


@app.get("/report/{hash}")
def get_report(hash: str):
    return FileResponse("index.html")
