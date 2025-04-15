import HERTA.Tools.IA as ia
from HERTA.Tools.Types.IA import IA_TYPE
import HERTA.Tools.Files as fl

class HERTA:
    def __init__(self, ia_type: IA_TYPE):
        match ia_type:
            case IA_TYPE.GEMINI:
                self.ia = ia.Gemini()
            case IA_TYPE.OLLAMA:
                self.ia = None
        pass

    def init(self):
        pass