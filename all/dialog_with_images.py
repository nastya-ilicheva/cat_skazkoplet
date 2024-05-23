from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import shutil
import base64
import requests
import uuid
from bs4 import BeautifulSoup
# from keys import *
import json
from IPython.display import display, Markdown

client_id = '518a13bd-22ca-4984-9ff0-c92be6e0f763'
secret = '38050be9-8a1f-4859-a1a6-a2abc3371637'
auth = 'NTE4YTEzYmQtMjJjYS00OTg0LTlmZjAtYzkyYmU2ZTBmNzYzOjM4MDUwYmU5LThhMWYtNDg1OS1hMWE2LWEyYWJjMzM3MTYzNw=='

credentials = f"{client_id}:{secret}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.
      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».
      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
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
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
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
        content="Ты александр пушкин, ты помогаешь детям писать сказки дополняя их предложения и художественно их окрашивая."
    )
]


def send_chat_request(giga_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Заголовки для HTTP-запроса
    headers = {
        'Content-Type': 'application/json',  # Указываем, что отправляемые данные в формате JSON
        'Authorization': f'Bearer {giga_token}',  # Используем токен авторизации для доступа к API
    }

    # Данные для отправки в теле запроса
    payload = {
        "model": "GigaChat:latest",  # Указываем, что хотим использовать последнюю версию модели GigaChat
        "messages": [
            {
                "role": "user",  # Роль отправителя - пользователь
                "content": user_message  # Сообщение от пользователя
            },
        ],
        "temperature": 0.7}  # Устанавливаем температуру, чтобы управлять случайностью ответов

    try:
        # Отправляем POST-запрос к API и получаем ответ
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        # Выводим текст ответа. В реальных условиях следует обрабатывать ответ и проверять статус коды.
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        # В случае возникновения исключения в процессе выполнения запроса, выводим ошибку
        print(f"Произошла ошибка: {str(e)}")
        return None


user_message = "Нарисуй оленя, праздник Новый Год, Аниме"
response_img_tag = send_chat_request(giga_token, user_message)
print(response_img_tag)

soup = BeautifulSoup(response_img_tag, 'html.parser')

# Извлекаем значение атрибута `src`
img_src = soup.img['src']

print(img_src)
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {giga_token}',
}

response = requests.get(f'https://gigachat.devices.sberbank.ru/api/v1/files/{img_src}/content', headers=headers,
                        verify=False)

with open('image4.jpg', 'wb') as f:
    f.write(response.content)



while (True):
    # Ввод пользователя
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot: ", res.content)
