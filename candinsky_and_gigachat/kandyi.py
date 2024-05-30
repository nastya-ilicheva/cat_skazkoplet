import base64
import json
import time
from data import db_session
from io import BytesIO
from PIL import Image
import requests
from candinsky_and_gigachat.giga import *
from random import randint


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def Base64(images, path):
    base64_string = str(images)
    img_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(img_data))
    image.save(path)


def _generate_image(prompt, path):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '36F323968BECBD8A0B08E0C2232FE262',
                        '0FF6B9AF488D717FD935E95727E9FF50')
    model_id = api.get_model()
    messages = [SystemMessage(content="Ты упрощаешь введенный текст. Убери все ненужное, но оставь описания.")]
    messages.append(HumanMessage(content=prompt))
    res = chat(messages)
    print(res.content)
    uuid = api.generate(f"{res.content}", model_id)
    images = api.check_generation(uuid)
    Base64(images, path)


def generate_image(prompt='', path=''):  # функция псевдогенерации
    time.sleep(randint(2, 7))
    return '../static/img/image2.png'


# url https://api-key.fusionbrain.ai/
# api_key C465EB979644D7D0B551F99A83583D21'
# secret '515C9E17AA663CA4A2E4B974C4BCB336'

if __name__ == "__main__":
    generate_image("Героиня сказки для детей в желтом платье", "test.png")
