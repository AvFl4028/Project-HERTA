from .Commands import Touch


class Files:
    def __init__(self):
        pass

    def write(self, msg: str, path: str):
        Touch(path)
        with open(path, "w", encoding="utf-8") as fl:
            fl.write(msg)
            fl.close()
