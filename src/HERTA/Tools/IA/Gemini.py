from .Base import Base
import google.genai as gemini
import ollama as llama
import os
import json
import logging
import datetime

# Create and configure logger
logging.basicConfig(
    filename=f"logs/{datetime.datetime.now()}.log", format="%(asctime)s %(message)s", filemode="w"
)

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


class Gemini:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API")
        self.client = gemini.Client(api_key=self.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"

    def consult(self, msg: str) -> str:
        if not msg or not self.GEMINI_API_KEY:
            return None

        prompt = (
            "Analiza cuidadosamente el siguiente mensaje del usuario e interpreta qué tipo de información necesita: "
            "puede ser un resumen, definición, explicación, comparación, parafraseo o investigación. "
            "Responde con la información solicitada de forma clara, precisa y completa, en formato Markdown. "
            "Utiliza párrafos bien estructurados, sin limitar la longitud si el tema lo requiere. "
            "Sé concreto, didáctico y profundo como si estuvieras explicándolo a un estudiante o profesional. "
            "Aquí está el mensaje del usuario:\n\n"
            f'"{msg}"'
        )

        response = self.__ask_model(prompt)
        return response

    def action(self, msg: str):

        prompt = (
            "Analiza el siguiente mensaje y deduce qué quiere hacer el usuario. "
            "Tu tarea es identificar la intención principal (por ejemplo: crear archivo, listar archivos, resumir texto, parafrasear, definir, etc.) "
            "y generar una respuesta en formato JSON con la siguiente estructura: "
            '{"texto": "lo que el usuario quiere hacer, como un resumen, parafraseo, etc.", '
            '"command": "uno de estos comandos: touch, list, concept", '
            '"file_name": "es caso de que sea el comando touch, aqui debe ir el nombre del archivo"'
            '"consulta": "el contenido específico que el usuario quiere investigar, consultar, resumir, etc."}. '
            "Regresa solo el JSON, sin ninguna explicación, en texto plano. Aquí está el mensaje del usuario:\n\n"
            + msg
        )

        raw_response: str = self.__ask_model(prompt=prompt)

        return self.__clean_json_response(response=raw_response)

    def statusMessage(self, msg: str, status: bool) -> str:
        prompt = (
            "Analiza el siguiente mensaje y deduce un mensaje en el cual me digas el estado de la accion a partir del valor de la variable, unicamente dame el mensaje, aqui esta el mensaje y variable: "
            f"{msg}"
            f"variable status: {status}"
        )

        logger.info(prompt)
        response = self.__ask_model(prompt)
        return response

    def response(self, msg: str) -> dict:
        accion = self.action(msg)
        accion["response"] = self.consult(accion["consulta"])
        accion["concept"] = self.concept(accion["consulta"])
        logger.info(accion)
        return accion

    def concept(self, msg: str):
        prompt = (
            "Dime un concepto, resumen o parafrasis corto segun lo deseado del siguiente mensaje, da el mensaje sin tu pensamiento o razonamiento de lo que quiere el usuario"
            "Mensaje: " + msg
        )

        response = self.__ask_model(prompt)
        return response

    def __ask_model(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            logger.info(response.text)
            return response.text
        except Exception as e:
            logger.error(f"[ask_model] {e}")
            return None

    def __clean_json_response(self, response: str) -> dict:
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