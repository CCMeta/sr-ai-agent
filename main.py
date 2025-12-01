import datetime
import ai
import db

from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    question = "请告诉我当前北京时间"
    # use python to print current time

    answer = question
    count = len(db.get())

    start_time = datetime.datetime.now()
    answer = ai.run(question)
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    return {
        "duration": duration,
        "content": question,
        "Answer": answer,
        "count": count,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}