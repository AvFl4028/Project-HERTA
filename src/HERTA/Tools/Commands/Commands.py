import subprocess
import os


class Commands:
    def __init__(self, command: str, args: str):
        self.command = command
        self.args = args

    def execute(self):
        return subprocess.run(
            f"{self.command} {self.args}",
            shell=True,
            check=True,
            capture_output=True,
            encoding="utf-8",
        ).stdout


class List(Commands):
    def __init__(self):
        super().__init__("", "")

    def execute(self, path: str = None):
        if path == "" or path == None:
            return os.listdir(".")
        return os.listdir(path)


class Touch(Commands):
    def __init__(self, path: str):
        super().__init__("touch", path)



def getPaths(path: str) -> list[str]:
    paths = []
    try:
        for mini_path in os.listdir(path):
            if mini_path != "venv" and mini_path != ".git" and mini_path != ".obsidian":
                full_path = os.path.join(path, mini_path)
            if os.path.isdir(full_path):
                paths.append(full_path)
                paths.extend(getPaths(full_path))

    except FileNotFoundError:
        return ["No hay archivos disponibles"]
    return paths


if __name__ == "__main__":
    Touch("./src/test.py").execute()
    for i in getPaths("/home/avfl/Documentos/Notas_ITO/Segundo Semestre"):
        print(i)
    pass
