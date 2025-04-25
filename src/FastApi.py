from fastapi import FastAPI, BackgroundTasks
import asyncio
from pydantic import BaseModel
from HERTA.HERTA import HERTA
from HERTA.Tools.Types.IA import IA_TYPE
from uuid import uuid4


class UserRequest(BaseModel):
    message: str


app = FastAPI()
herta = HERTA(IA_TYPE.GEMINI, debug=True)

message: str = None


@app.get("/")
def status_handler():
    return {"status": "OK"}


@app.post("/post")
def post_handler(req: UserRequest, bg: BackgroundTasks):
    global message
    message = "Waiting..."
    bg.add_task(response_task, req.message)
    return {"status": req.message != None}


@app.get("/get")
def get_handler():
    global message
    return {"message": message}


def response_task(msg: str):
    global message
    herta.setMessage(msg)
    response_status: bool = herta.loadResponse()
    if response_status:
        message = herta.getStatusMessage(herta.action())
