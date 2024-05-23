from giga import *
import json
from create_prompt_for_kandy import create_for_k


def create_json(prompt):
    # Ввод пользователя
    user_input = prompt
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot character: ", res.content)
    create_for_k(prompt, res.content)


messages = [
    SystemMessage(
        content="Ты должен на основе ответа пользователя создать json файл с описанием внешности персонажа. В  json "
                "не должно быть длинных описаний, максимум 2 слова. все на английском языке. обязательны поля: type, "
                "sex, description, biometric_data, physical_features, appearance, speech, personality type,"
                "habits, phobias, features, family, friends, important_life_events, another\nкаждый раз после запроса"
                "ты будешь дополнять файл\nесли персонажей несколько создавай для каждого свой json файл, выводи в"
                "ответ каждый\njson только на английском\njson составляется только для главных действующих лиц"
    )
]

if __name__ == "__main__":
    print("Опиши, пожалуйста, как будет выглядеть персонаж твоей истории.")



