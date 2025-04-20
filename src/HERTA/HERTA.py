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

        self.__message: str
        self.__response: dict

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

    def setMessage(self, msg):
        if msg != None:
            self.__message = msg
            return True
        return False

    def loadResponse(self):
        try:
            self.__response = self.ia.response(self.message)
            return True
        except:
            return False

    def getResponse(self):
        return self.response["response"]

    def action(self) -> bool:
        if self.response["command"] == "touch":
            file = os.path.join(self.path, self.response["file_name"])
            Files().write(self.response["response"], file)
            return True
        return False
