import HERTA.Tools.IA as ia
from HERTA.Tools.Types.IA import IA_TYPE
from HERTA.Tools.Files import Files
import os
from dotenv import load_dotenv

load_dotenv()


class HERTA:
    def __init__(self, ia_type: IA_TYPE, debug: bool = False):
        if debug:
            self.path = os.getenv("DEBUG_PATH")
        else:
            self.path = "."

        match ia_type:
            case IA_TYPE.GEMINI:
                self.ia = ia.Gemini()
            case IA_TYPE.OLLAMA:
                self.ia = None

    def init(self):
        salir = False
        try:
            while not salir:
                response = self.ia.response(input("¿Qué quieres hacer?\n"))
                if response["command"] == "touch":
                    file = os.path.join(self.path, response["file_name"])
                    Files().write(response["response"], file)
        except KeyboardInterrupt:
            print("\nHasta luego!")

    def godot(self, msg: str):
        print(msg)
        response = self.ia.response(msg)
        print(response)
        if response["command"] == "touch":
            file = os.path.join(self.path, response["file_name"])
            Files().write(response["response"], file)
        
        return "Todo bien :3"
