from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from gigachat.models.usage import Usage
from langchain.chat_models.gigachat import GigaChat
import base64
import requests
import uuid
# from keys import *
import json

def init_giga():

    client_id = '6c6a3558-8e36-4350-8d21-fa3a31b4688f'
    secret = '1c73028a-d00f-476d-8041-c25e39f73bf3'
    auth = 'NmM2YTM1NTgtOGUzNi00MzUwLThkMjEtZmEzYTMxYjQ2ODhmOjFjNzMwMjhhLWQwMGYtNDc2ZC04MDQxLWMyNWUzOWY3M2JmMw=='

    credentials = f"{client_id}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    response = get_token(auth)
    if response != 1:
        # print(response.text)
        giga_token = response.json()['access_token']

    models(giga_token)

    return GigaChat(credentials=auth, verify_ssl_certs=False)


def models(giga_token):
    url_models = "https://gigachat.devices.sberbank.ru/api/v1/models"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {giga_token}'
    }

    response = requests.request("GET", url_models, headers=headers, data=payload, verify=False)
    # print(response.text)
    return response.text

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








# messages = [
#     SystemMessage(
#         content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
#     )
# ]


if __name__ == '__main__':
#     test = """
#     [SystemMessage(content='Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения.')]
#     [SystemMessage(content='Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения.'), AIMessage(content='Однажды, когда на улице было очень холодно, маленький котёнок решил спрятаться в коробке. Он думал, что там будет тепло и уютно. Но вдруг он услышал странный звук. Это был голос мыши. Мышь сказала: "Привет, малыш! Я тоже хочу быть с тобой в этой коробке". Котёнку стало немного страшно, но он всё равно согласился. Они стали играть вместе и веселиться. И так они стали лучшими друзьями.', response_metadata={'token_usage': Usage(prompt_tokens=26, completion_tokens=110, total_tokens=136), 'model_name': 'GigaChat:3.1.25.3', 'finish_reason': 'stop'}, id='run-d28fa34f-63e0-44f0-ad93-0610ddf9dda2-0')]
# """
#     t = eval (test)
    messages = []
    chat = init_giga()
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
