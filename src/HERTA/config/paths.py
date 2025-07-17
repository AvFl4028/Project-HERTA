import json
import os

__values = open("src/HERTA/config/paths.json", "r", encoding="utf-8")
__json = json.loads(__values.read())

def downloadsPath() -> str:
    return __json["descargas"]

def documentsPath() -> str:
    return __json["documentos"]

def algebraPath() -> str:
    return documentsPath() + __json["algebra"]

def integralPath() -> str:
    return documentsPath() + __json["integral"]

def quimicaPath() -> str:
    return documentsPath() + __json["quimica"]

def probabilidadPath() -> str:
    return documentsPath() + __json["probabilidad"]

def pooPath() -> str:
    return documentsPath() + __json["poo"]


def main():
    print(os.listdir(downloadsPath()))
    print()
    print(os.listdir(documentsPath()))
    print()
    print(os.listdir(pooPath()))
    print()
    print(os.listdir(algebraPath()))
    print()
    print(os.listdir(integralPath()))
    print()
    print(os.listdir(quimicaPath()))
    print()
    print(os.listdir(probabilidadPath()))
    print()
if __name__ == "__main__":
    main()