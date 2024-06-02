import base64
import json
import time
from io import BytesIO
from PIL import Image
import requests


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

    def generate(self, prompt, model, images=1, width=400, height=400):
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


def create_picture(prompt):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'C465EB979644D7D0B551F99A83583D21',
                        '515C9E17AA663CA4A2E4B974C4BCB336')
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)
    print("картинка создана!")
    Base64(images)


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'C465EB979644D7D0B551F99A83583D21',
                        '515C9E17AA663CA4A2E4B974C4BCB336')
    model_id = api.get_model()
    uuid = api.generate("милая девушка с большими голубыми глазами в полный рост; стиль: акварельная картина", model_id)
    images = api.check_generation(uuid)
    print(images)


def Base64(images):
    base64_string = str(images)
    img_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(img_data))
    image.show()
    image.save('image4.png')
    # image.save('output.jpg', 'JPEG')


# url https://api-key.fusionbrain.ai/
# api_key C465EB979644D7D0B551F99A83583D21'
# secret '515C9E17AA663CA4A2E4B974C4BCB336'
# Base64()