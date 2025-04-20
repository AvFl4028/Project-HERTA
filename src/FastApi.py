from fastapi import FastAPI
from pydantic import BaseModel
from HERTA.HERTA import HERTA
from HERTA.Tools.Types.IA import IA_TYPE


class UserRequest(BaseModel):
    message: str


app = FastAPI()
herta = HERTA(IA_TYPE.GEMINI, debug=True)

@app.get("/")
def status_handler():
    return {"status": "OK"}


@app.post("/post")
def post_handler(req: UserRequest):
    if herta.setMessage(req.message):
        return {"status": "ok"}
    return {"status": "error"}

@app.get("/loadResponse")
def loadResponse_handler():
    if herta.loadResponse():
        return {"status": "OK"}
    return {"status": "error"}

@app.get("/response")
async def response_handler():
    return {"response": herta.getResponse()}

@app.get("/action")
def action_handler():
    return {"status": herta.action()}