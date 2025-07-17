from HERTA.HERTA import HERTA as herta
from HERTA.Tools.Types.IA import IA_TYPE
import uvicorn
import sys
import os

# Agrega 'src' al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    uvicorn.run("api.FastApi:app", host="0.0.0.0", port=8000, reload=True)
    # bot = herta(IA_TYPE.GEMINI, debug=True)
    # bot.init()


if __name__ == "__main__":
    main()
