from giga import *
from character import create_json

messages = [
    SystemMessage(
        content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
    )
]

while (True):
    # Ввод пользователя
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot: ", res.content)
    create_json(user_input + res.content)

