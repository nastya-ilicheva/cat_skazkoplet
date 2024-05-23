from giga import *
import json
from kandyi import generate_image

messages = [
        SystemMessage(
            content=f"Ты создаешь описание персонажа на основании json файла (если json файлов несколько, то описывай "
                    f"всех персонажей) и описания происходящего\nесли данных недостаточно, не используй их\nочень "
                    f"коротко, литературно"
        )
    ]
def create_for_k(description, prompt):
    # Reading from file
    character = prompt

    # Ввод пользователя и сохранение json описания
    # user_input = input("User: ")
    messages.append(HumanMessage(content=f"{character} {description}"))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot for picture: ", res.content)
    generate_image(res.content)


