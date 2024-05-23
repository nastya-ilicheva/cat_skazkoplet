from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import shutil
import base64
import requests
import openai
from bs4 import BeautifulSoup
import uuid
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
    print(giga_token)

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

# def get_chat_completion(auth_token, user_message):
#     """
#     Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.
#
#     Параметры:
#     - auth_token (str): Токен для авторизации в API.
#     - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.
#
#     Возвращает:
#     - str: Ответ от API в виде текстовой строки.
#     """
#     # URL API, к которому мы обращаемся
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#
#     # Подготовка данных запроса в формате JSON
#     payload = json.dumps({
#         "model": "GigaChat",  # Используемая модель
#         "messages": [
#             {
#                 "role": "user",  # Роль отправителя (пользователь)
#                 "content": user_message  # Содержание сообщения
#             }
#         ],
#         "temperature": 1,  # Температура генерации
#         "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
#         "n": 1,  # Количество возвращаемых ответов
#         "stream": False,  # Потоковая ли передача ответов
#         "max_tokens": 512,  # Максимальное количество токенов в ответе
#         "repetition_penalty": 1,  # Штраф за повторения
#         "update_interval": 0  # Интервал обновления (для потоковой передачи)
#     })
#
#     # Заголовки запроса
#     headers = {
#         'Content-Type': 'application/json',  # Тип содержимого - JSON
#         'Accept': 'application/json',  # Принимаем ответ в формате JSON
#         'Authorization': f'Bearer {auth_token}'  # Токен авторизации
#     }
#
#     # Выполнение POST-запроса и возвращение ответа
#     try:
#         response = requests.request("POST", url, headers=headers, data=payload, verify=False)
#         return response
#     except requests.RequestException as e:
#         # Обработка исключения в случае ошибки запроса
#         print(f"Произошла ошибка: {str(e)}")
#         return -1
#
#
# answer = get_chat_completion(giga_token, 'расскажи мне 1 закон ньютона как пятилетнему ребенку')
# answer.json()
#
# print(answer.json()['choices'][0]['message']['content'])
#
# display(Markdown(answer.json()['choices'][0]['message']['content']))


# def get_chat_completion(auth_token, user_message, conversation_history=None):
#     """
#     Отправляет POST-запрос к API чата для получения ответа от модели GigaChat в рамках диалога.
#
#     Параметры:
#     - auth_token (str): Токен для авторизации в API.
#     - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.
#     - conversation_history (list): История диалога в виде списка сообщений (опционально).
#
#     Возвращает:
#     - response (requests.Response): Ответ от API.
#     - conversation_history (list): Обновленная история диалога.
#     """
#     # URL API, к которому мы обращаемся
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#
#     # Если история диалога не предоставлена, инициализируем пустым списком
#     if conversation_history is None:
#         conversation_history = []
#
#     # Добавляем сообщение пользователя в историю диалога
#     conversation_history.append({
#         "role": "user",
#         "content": user_message
#     })
#
#     # Подготовка данных запроса в формате JSON
#     payload = json.dumps({
#         "model": "GigaChat:latest",
#         "messages": conversation_history,
#         "temperature": 1,
#         "top_p": 0.1,
#         "n": 1,
#         "stream": False,
#         "max_tokens": 512,
#         "repetition_penalty": 1,
#         "update_interval": 0
#     })
#
#     # Заголовки запроса
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': f'Bearer {auth_token}'
#     }
#
#     # Выполнение POST-запроса и возвращение ответа
#     try:
#         response = requests.post(url, headers=headers, data=payload, verify=False)
#         response_data = response.json()
#         print(response_data)
#
#         # Добавляем ответ модели в историю диалога
#         conversation_history.append({
#             "role": "assistant",
#             "content": response_data['choices'][0]['message']['content']
#         })
#
#         return response, conversation_history
#     except requests.RequestException as e:
#         # Обработка исключения в случае ошибки запроса
#         print(f"Произошла ошибка: {str(e)}")
#         return None, conversation_history
#
#
# conversation_history = []
# #user_message = input()
# # Пользователь отправляет первое сообщение
# response, conversation_history = get_chat_completion(giga_token, user_message, conversation_history)
#
# # Пользователь отправляет следующее сообщение, продолжая диалог
# response, conversation_history = get_chat_completion(giga_token, user_message, conversation_history)

# print(conversation_history)


chat = GigaChat(credentials=auth, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
    )
]



headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {giga_token}',
}

json_data = {
    'model': 'GigaChat',
    'messages': [
        {
            'role': 'system',
            'content': 'Ты профессиональный художник. Если тебя просят создать изображение, ты должен сгенерировать специальный блок: <fuse>text2image(query: str, style: str)</fuse>,\nгде query — логотип моей компании, которая занимается производством корма для котов, style — абстракция.',
        },
    ],
    'temperature': 1,
    'top_p': 0.1,
    'n': 1,
    'stream': False,
    'max_tokens': 512,
    'repetition_penalty': 1,
    'update_interval': 0,
}

response = requests.post('https://gigachat.devices.sberbank.ru/api/v1/chat/completions', headers=headers, json=json_data, verify=False)
# print(response.json())
#
# id = response.json()['choices'][0]['message']['content']
# print(id)
#

response_img_tag = response.json()["choices"][0]["message"]["content"]
print(response_img_tag)
print(response.json()['created'])
id = response.json()['created']
print(response.json())


def generate_images(prompt, n_images=4, size="512x512"):
    r = openai.Image.acreate(prompt=prompt, n=n_images, size=size)
    image_urls = [item.url for item in r.data]
    return image_urls



# soup = BeautifulSoup(id, 'html.parser')
#
#
# img_src = soup.img['src']
#
# print(img_src)
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {giga_token}',
# }

response1 = requests.get(f'https://gigachat.devices.sberbank.ru/api/v1/files/{id}/content', headers=headers,
                        verify=False)

with open('image4.jpg', 'wb') as f:
    f.write(response1.content)



url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{id}/content"

headers = {
  'Accept': 'application/jpg',
  'Authorization': f'Bearer {giga_token}'
}

response = requests.request("GET", url, headers=headers, stream=True, verify=False)

with open('9.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

#
#
# while (True):
#     # Ввод пользователя
#     user_input = input("User: ")
#     messages.append(HumanMessage(content=user_input))
#     res = chat(messages)
#     messages.append(res)
#     # Ответ модели
#     print("Bot: ", res.content)