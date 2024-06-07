from giga import *
import json
from create_prompt_for_kandy import create_for_k
#в этой папке навсе для рисвоания

def create_json(prompt):
    # Ввод пользователя
    user_input = prompt
    messages.append(HumanMessage(content=AIMessage))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot character: ", res.content)
    create_for_k(prompt, res.content)


messages = [
    SystemMessage(
        content="Ты должен на основе ответа пользователя создать json файл с описанием внешности персонажа."
                " В  json. обязательны поля: type, "
                " another\nкаждый раз после запроса"
                "ты будешь дополнять файл\nесли персонажей несколько создавай для каждого свой json файл, выводи в"
                "ответ каждый\nпакуй в json, \njson составляется только для главных действующих лиц"
    )
]

if __name__ == "__main__":
    print("Опиши, пожалуйста, как будет выглядеть персонаж твоей истории.")



