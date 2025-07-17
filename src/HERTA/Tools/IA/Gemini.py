from .Base import Base
import google.genai as gemini
import ollama as llama
import os
import json
import datetime
from ...config.logger import setup_logger


# Creating an object
logger = setup_logger(__name__)

class Gemini(Base):
    def __init__(self):
        super().__init__()
        self.GEMINI_API_KEY = os.getenv("GEMINI_API")
        self.client = gemini.Client(api_key=self.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"

    def consult(self, msg: str) -> str:
        if not msg or not self.GEMINI_API_KEY:
            return None

        response = self._ask_model(self.consult_prompt(msg))
        logger.info("Consulta generada!")

        return response

    def action(self, msg: str):
        raw_response: str = self._ask_model(prompt=self.action_prompt(msg))
        logger.info("Action generada!")
        return self._clean_json_response(response=raw_response)

    def statusMessage(self, msg: str, status: bool) -> str:
        response = self._ask_model(self.status_prompt(msg, status))
        logger.info("Mensaje de status generado")
        return response

    def response(self, msg: str) -> dict:
        accion = self.action(msg)
        accion["response"] = self.consult(accion["consulta"])
        accion["concept"] = self.concept(accion["consulta"])
        logger.info("Respuesta generada")
        return accion

    def concept(self, msg: str):
        response = self._ask_model(self.concept_prompt(msg))
        logger.info("Concepto generado")
        return response

    def _ask_model(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            logger.info("Respuesta del modelo generada")
            return response.text
        except Exception as e:
            logger.error(f"[ask_model] {e}")
            return None

    def _clean_json_response(self, response: str) -> dict:
        try:
            cleaned = response.replace("```", "").replace("json", "").strip()
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"[clean_json_response] {e}")
            return {}


if __name__ == "__main__":
    print(
        Gemini().consult(
            Gemini().action(input("Escribe lo que quieres saber: "))["consulta"]
        )
    )
