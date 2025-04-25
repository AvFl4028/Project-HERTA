from HERTA.HERTA import HERTA as herta
from HERTA.Tools.Types.IA import IA_TYPE


def main():
    bot = herta(IA_TYPE.GEMINI, debug=True)
    bot.init()


if __name__ == "__main__":
    main()
