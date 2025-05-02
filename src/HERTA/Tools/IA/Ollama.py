from .Base import Base
from ollama import chat, ChatResponse
import ollama as llama
from ...config.logger import setup_logger
import json

log = setup_logger(__name__)

class Ollama(Base):
    def __init__(self, model: str):
        self.__model = model
        super().__init__()

    def _ask_model(self, msg: str) -> str:
        try:
            response_stream = chat(
                model=self.__model,
                messages=[{"role": "user", "content": msg}],
                stream=True,
            )
            response: str = ""

            for chunk in response_stream:
                response += chunk["message"]["content"]
                # print(chunk["message"]["content"], end="", flush=True)
                log.info(chunk["message"]["content"])

            return response
        except:
            log.error("Error en ollama ask model")
            return ""

    def consult(self, msg: str) -> str:
        return self._ask_model(self.consult_prompt(msg))

    def action(self, msg: str) -> str:
        raw_response: str = self._ask_model(self.action_prompt(msg))
        return self._clean_json_response(response=raw_response)

    def statusMessage(self, msg: str, status: bool) -> str:
        return self._ask_model(self.status_prompt(msg, status))

    def response(self, msg: str) -> dict:
        accion = self.action(msg)
        accion["response"] = self.consult(accion["consulta"])
        accion["concept"] = self.concept(accion["consulta"])
        log.info(accion)
        return accion

    def concept(self, msg):
        return self._ask_model(self.concept_prompt(msg))

    def _clean_json_response(self, response: str) -> dict:
        try:
            cleaned = response.replace("```", "").replace("json", "").strip()
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            log.error(f"[clean_json_response] {e}")
            return {}


if __name__ == "__main__":
    models = json.loads(llama.list().model_dump_json())["models"]
    # for i in models:
    #     print(i["model"])
    assit = Ollama(model=models[1]["model"])
    print(
        assit.response(
            "Crea un archivo assistance.md que tenga lo basico de lo que tu puedes hacer como asistente"
        )
    )
