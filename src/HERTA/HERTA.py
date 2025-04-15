import HERTA.Tools.IA as ia
from HERTA.Tools.Types.IA import IA_TYPE
from HERTA.Tools.Commands.Commands import Touch
import os
class HERTA:
    def __init__(self, ia_type: IA_TYPE):
        match ia_type:
            case IA_TYPE.GEMINI:
                self.ia = ia.Gemini()
            case IA_TYPE.OLLAMA:
                self.ia = None

    def init(self):
        try:
            while True:
                response = self.ia.response(input("¿Qué quieres hacer?\n"))
                if response["command"] == "touch":
                    file = os.path.join(".", response["file_name"])
                    Touch(file)
                    with open(file, "w", encoding="utf-8") as fl:
                        fl.write(response["response"])
        except KeyboardInterrupt:
            print("\nHasta luego!")