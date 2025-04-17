from fastapi import FastAPI
from pydantic import BaseModel
from HERTA.HERTA import HERTA
from HERTA.Tools.Types.IA import IA_TYPE


class UserRequest(BaseModel):
    message: str


app = FastAPI()


@app.get("/")
def status_handler():
    return {"status": "OK"}


@app.post("/post")
def post_handler(req: UserRequest):
    print(req.message)
    response = HERTA(ia_type=IA_TYPE.GEMINI, debug=True).godot(req.message)
    return {"response": response}
