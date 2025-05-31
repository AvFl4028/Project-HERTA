from fastapi import FastAPI, BackgroundTasks
import asyncio
from pydantic import BaseModel
from ..HERTA import HERTA
from ..HERTA.Tools import IA_TYPE
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from ..HERTA.config.logger import setup_logger

setup_logger(__name__)

class UserRequest(BaseModel):
    message: str


class ConfigReq(BaseModel):
    ia_type: IA_TYPE
    debug: bool


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # También puedes usar ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

herta: HERTA

message: str
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


@app.post("/assistant/config")
def assistantConfig(req: ConfigReq):
    global herta
    try:
        herta = HERTA(req.ia_type, debug=req.debug)
        return {"status": True}
    except:
        return {"status": False}


def response_task(msg: str):
    global message
    global msg_ready

    msg_ready = False
    herta.setMessage(msg)
    response_status: bool = herta.loadResponse()
    if response_status:
        message = herta.getStatusMessage(herta.action())

    msg_ready = True
