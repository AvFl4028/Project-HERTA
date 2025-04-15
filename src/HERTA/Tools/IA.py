import google.genai as gemini
import ollama as llama
import os


class Gemini:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API")
        self.client = gemini.Client(api_key=self.GEMINI_API_KEY)

    def consult(self, msg: str) -> str:
        if msg == None or msg == "" or self.GEMINI_API_KEY == None:
            return None

        return self.client.models.generate_content(
            model="gemini-2.0-flash", contents=f'Dame lo que el siguiente texto te va a pedir: "{msg}"'
        ).text
    
    def action(self, msg: str):
        return self.client.models.generate_content(
            model="gemini-2.0-flash", contents=f'Dame lo que el siguiente texto te va a pedir: "{msg}"'
        ).text


if __name__ == "__main__":
    print(Gemini().consult(input("Escribe lo que quieres saber: ")))
