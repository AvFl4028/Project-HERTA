import google.genai as gemini
import ollama as llama
import os
import json


class Gemini:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API")
        self.client = gemini.Client(api_key=self.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"

    def consult(self, msg: str) -> str:
        if msg == None or msg == "" or self.GEMINI_API_KEY == None:
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

        return self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        ).text

    def action(self, msg: str):

        prompt = (
            "Analiza el siguiente mensaje y deduce qué quiere hacer el usuario. "
            "Tu tarea es identificar la intención principal (por ejemplo: crear archivo, listar archivos, resumir texto, parafrasear, definir, etc.) "
            "y generar una respuesta en formato JSON con la siguiente estructura: "
            '{"texto": "lo que el usuario quiere hacer, como un resumen, parafraseo, etc.", '
            '"command": "uno de estos comandos: touch, list", '
            '"file_name": "es caso de que sea el comando touch, aqui debe ir el nombre del archivo"'
            '"consulta": "el contenido específico que el usuario quiere investigar, consultar, resumir, etc."}. '
            "Regresa solo el JSON, sin ninguna explicación, en texto plano. Aquí está el mensaje del usuario:\n\n"
            + msg
        )

        return (
            self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            .text.replace("```", "")
            .replace("json", "")
        )

    def response(self, msg: str) -> dict:

        accion = json.loads(self.action(msg))
        accion["response"] = self.consult(accion["consulta"])
        return accion


if __name__ == "__main__":
    print(
        Gemini().consult(
            json.loads(Gemini().action(input("Escribe lo que quieres saber: ")))[
                "consulta"
            ]
        )
    )
