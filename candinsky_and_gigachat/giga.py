from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from gigachat.models.usage import Usage
from langchain.chat_models.gigachat import GigaChat

import base64
import requests
import uuid
# from keys import *
import json


client_id = '518a13bd-22ca-4984-9ff0-c92be6e0f763'
secret = '38050be9-8a1f-4859-a1a6-a2abc3371637'
auth = 'NTE4YTEzYmQtMjJjYS00OTg0LTlmZjAtYzkyYmU2ZTBmNzYzOjM4MDUwYmU5LThhMWYtNDg1OS1hMWE2LWEyYWJjMzM3MTYzNw=='

credentials = f"{client_id}:{secret}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'}

    # Тело запроса
    payload = {'scope': scope}

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


response = get_token(auth)
if response != 1:
    # print(response.text)
    giga_token = response.json()['access_token']


def models():
    url_models = "https://gigachat.devices.sberbank.ru/api/v1/models"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {giga_token}'
    }

    response = requests.request("GET", url_models, headers=headers, data=payload, verify=False)
    # print(response.text)
    return response.text


models()


chat = GigaChat(credentials=auth, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
    )
]


if __name__ == '__main__':
    test = """
    [SystemMessage(content='Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения.')]
    [SystemMessage(content='Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения.'), AIMessage(content='Однажды, когда на улице было очень холодно, маленький котёнок решил спрятаться в коробке. Он думал, что там будет тепло и уютно. Но вдруг он услышал странный звук. Это был голос мыши. Мышь сказала: "Привет, малыш! Я тоже хочу быть с тобой в этой коробке". Котёнку стало немного страшно, но он всё равно согласился. Они стали играть вместе и веселиться. И так они стали лучшими друзьями.', response_metadata={'token_usage': Usage(prompt_tokens=26, completion_tokens=110, total_tokens=136), 'model_name': 'GigaChat:3.1.25.3', 'finish_reason': 'stop'}, id='run-d28fa34f-63e0-44f0-ad93-0610ddf9dda2-0')]
"""
    t = eval (test)
    while (True):
        # Ввод пользователя
        user_input = input("User: ")
        messages.append(HumanMessage(content=user_input))
        res = chat(messages)
        print(type(res.response_metadata["token_usage"]))
        messages.append(res)
        print(messages)
        # Ответ модели
        print("Bot: ", res.content)
