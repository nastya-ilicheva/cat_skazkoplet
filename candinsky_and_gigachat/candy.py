import base64
import json
from io import BytesIO
from PIL import Image
import aiohttp
import asyncio
import aiofiles
import requests

API_KEY = '36F323968BECBD8A0B08E0C2232FE262'
SECRET_KEY = '0FF6B9AF488D717FD935E95727E9FF50'


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    async def get_model(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS) as response:
                data = await response.json()
                return data[0]['id']

    # async def generate(self, prompt, model, images=1, width=1024, height=1024):
    #     params = {
    #         "type": "GENERATE",
    #         "numImages": images,
    #         "width": width,
    #         "height": height,
    #         "generateParams": {
    #             "query": f"{prompt}"
    #         }
    #     }
    #
    #     # data = aiohttp.FormData()
    #     # data.add_field('model_id', model)
    #     # data.add_field('params', json.dumps(params), content_type='application/json')
    #     #
    #     # print(model)
    #     data = {
    #         'model_id': (None, model),
    #         'params': (None, json.dumps(params), 'application/json')
    #     }
    #
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS,
    #                                 data=data) as response:
    #             data = await response.json()
    #             print(data)
    #             return data['uuid']

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

    async def check_generation(self, request_id, attempts=10, delay=10):
        async with aiohttp.ClientSession() as session:
            while attempts > 0:
                async with session.get(self.URL + 'key/api/v1/text2image/status/' + request_id,
                                       headers=self.AUTH_HEADERS) as response:
                    data = await response.json()
                    print(data['status'])
                    if data['status'] == 'DONE':
                        return data['images']
                attempts -= 1
                await asyncio.sleep(delay)


def Base64(images, path):
    base64_string = str(images)
    img_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(img_data))
    image.save(path)


async def generate_image(prompt, path):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)

    # Получение идентификатора модели
    model_id = await api.get_model()

    # Генерация изображения на основе модели и запроса
    uuid = api.generate(prompt, model_id)

    # Проверка статуса генерации
    images = await api.check_generation(uuid)

    # Сохранение изображения в файл
    Base64(images, path)


if __name__ == "__main__":
    prompt = "Героиня сказки для детей в зеленом платье"
    path = "test.png"
    asyncio.run(generate_image(prompt, path))
