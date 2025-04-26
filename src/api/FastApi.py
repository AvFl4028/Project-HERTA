from fastapi import FastAPI, BackgroundTasks
import asyncio
from pydantic import BaseModel
from ..HERTA import HERTA
from ..HERTA.Tools import IA_TYPE
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware


class UserRequest(BaseModel):
    message: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # También puedes usar ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

herta = HERTA(IA_TYPE.GEMINI, debug=True)

message: str = None
msg_ready: bool = False


@app.get("/")
def status_handler():
    return {"status": "OK"}


@app.post("/post")
async def post_handler(req: UserRequest, bg: BackgroundTasks):
    global message
    message = "Waiting..."
    bg.add_task(response_task, req.message)
    return {"status": req.message != None}


@app.get("/get")
def get_handler():
    return {"ready": msg_ready}


@app.get("/assistant/response")
def assistantHandler():
    return {"message": message}


def response_task(msg: str):
    global message
    global msg_ready

    msg_ready = False
    herta.setMessage(msg)
    response_status: bool = herta.loadResponse()
    if response_status:
        message = herta.getStatusMessage(herta.action())
    
    msg_ready = True
