from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from gigachat.models.usage import Usage
from langchain.chat_models.gigachat import GigaChat
import base64
import requests
import uuid

import json

client_id = '2b8cbc9f-752b-4b0f-b461-13bc317c9b03'
secret = '9c02d4bb-6ecc-4e98-a945-e02859549ae4'
auth = 'MmI4Y2JjOWYtNzUyYi00YjBmLWI0NjEtMTNiYzMxN2M5YjAzOjljMDJkNGJiLTZlY2MtNGU5OC1hOTQ1LWUwMjg1OTU0OWFlNA=='


def init_giga():
    credentials = f"{client_id}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    response = get_token(auth)
    if response != 1:
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


def main():
    messages = []
    chat = init_giga()
    while True:
        # Ввод пользователя
        user_input = input("User: ")
        messages.append(HumanMessage(content=user_input))
        res = chat(messages)
        print(type(res.response_metadata["token_usage"]))
        messages.append(res)
        print(messages)
        # Ответ модели
        print("Bot: ", res.content)


if __name__ == '__main__':
    main()
