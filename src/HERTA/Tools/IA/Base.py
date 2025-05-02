from abc import ABC, abstractmethod


class Base(ABC):
    # Prompts
    __CONSULT_PROMPT: str = (
        "Analiza cuidadosamente el siguiente mensaje del usuario e interpreta qué tipo de información necesita: "
        "puede ser un resumen, definición, explicación, comparación, parafraseo o investigación. "
        "Responde con la información solicitada de forma clara, precisa y completa, en formato Markdown. "
        "Utiliza párrafos bien estructurados, sin limitar la longitud si el tema lo requiere. "
        "Sé concreto, didáctico y profundo como si estuvieras explicándolo a un estudiante o profesional. "
        "Aquí está el mensaje del usuario:\n\n"
    )

    __ACTION_PROMPT: str = (
        "Analiza el siguiente mensaje y deduce qué quiere hacer el usuario. "
        "Tu tarea es identificar la intención principal (por ejemplo: crear archivo, listar archivos, resumir texto, parafrasear, definir, etc.)"
        "y generar una respuesta en formato JSON con la siguiente estructura: "
        '{"texto": "lo que el usuario quiere hacer, como un resumen, parafraseo, etc.", '
        '"command": "uno de estos comandos: touch, list, concept", '
        '"file_name": "es caso de que sea el comando touch, aqui debe ir el nombre del archivo",'
        '"consulta": "el contenido específico del tema que el usuario quiere investigar, consultar, resumir, etc. (Obligatorio que tenga más de 10 palabras)"}. '
        "Regresa solo el JSON, sin ninguna explicación, es obligatorio que ningun campo quede vacio,en texto plano. Aquí está el mensaje del usuario:\n\n"
    )

    __CONCEPT_PROMPT: str = (
        "Dime un concepto, resumen o parafrasis corto segun lo deseado del siguiente mensaje, da el mensaje sin tu pensamiento o razonamiento de lo que quiere el usuario"
        "Mensaje: "
    )

    __STATUS_PROMPT: str = (
        "Analiza el siguiente mensaje y deduce un mensaje en el cual me digas el estado de la accion a partir del valor de la variable, unicamente dame el mensaje, aqui esta el mensaje y variable: "
    )

    # Prompts Getters

    @staticmethod
    def consult_prompt(msg: str) -> str:
        return Base.__CONSULT_PROMPT + msg

    @staticmethod
    def action_prompt(msg: str) -> str:
        return Base.__ACTION_PROMPT + msg

    @staticmethod
    def concept_prompt(msg: str) -> str:
        return Base.__CONCEPT_PROMPT + msg

    @staticmethod
    def status_prompt(msg: str, status: bool):
        return Base.__STATUS_PROMPT + (f"{msg}" f"variable status: {status}")

    # Metodos abstractos
    @abstractmethod
    def _ask_model(self, msg: str) -> str:
        pass

    @abstractmethod
    def consult(self, msg: str) -> str:
        pass

    @abstractmethod
    def action(self, msg: str) -> str:
        pass

    @abstractmethod
    def statusMessage(self, msg: str, status: bool) -> str:
        pass

    @abstractmethod
    def response(self, msg: str) -> dict:
        pass

    @abstractmethod
    def concept(self, msg: str) -> str:
        pass

    @abstractmethod
    def _clean_json_response(self, response: str) -> dict:
        pass


if __name__ == "__main__":
    print(type(Base.concept_prompt("")))
