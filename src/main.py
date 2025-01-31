from ollama import Client


def main():
    HERTA = Client()
    model_name = "deepseek-r1:1.5b"
    herta = HERTA.create(
        model="HERTA",
        from_=model_name,
        system="You are a AI assistant that can edit files in the system",
    )
    print(herta.status)

    herta_chat = HERTA.chat(
        model="HERTA", messages=[{"role": "assistant", "content": "What are you?"}]
    )

    print(herta_chat.message.content)



if __name__ == "__main__":
    main()
