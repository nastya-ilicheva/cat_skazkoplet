import base64
import json
from io import BytesIO
from PIL import Image
import aiohttp
import asyncio
import aiofiles
import requests
import replicate
import os
from translate import Translator


API_KEY = '36F323968BECBD8A0B08E0C2232FE262'
SECRET_KEY = '0FF6B9AF488D717FD935E95727E9FF50'
os.environ["REPLICATE_API_TOKEN"] = "r8_Y1piYSDyvntnHRa8nZ0pQbEMoSvr8nT4MtM1r"



class Text2ImageAPI:

    def translate_text(self, text):
        translator = Translator(from_lang="ru", to_lang="en")
        translation = translator.translate(text)
        return translation


    def create_image(self, promt, width=512, height=512, num_pictures=1):
        promt = self.translate_text(promt) + 'there must not  be words in the picture'
        input = {
            "width": width,
            "height": height,
            "prompt": promt,
            "refine": "expert_ensemble_refiner",
            "apply_watermark": False,
            "num_inference_steps": 25,
            "num_outputs": num_pictures
        }

        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input=input
        )
        return output[0]




    async def check_generation(self, request_id, attempts=10, delay=10):
        async with aiohttp.ClientSession() as session:
            while attempts > 0:
                async with session.get(self.create_image) as response:
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

def save_image(url, path):
    response = requests.get(url)


    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    else:
        print('Failed to download file')

async def generate_image_new(prompt, path):
    tti = Text2ImageAPI()
    images = tti.create_image(prompt)
    print(images)
    # api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    #
    # # Получение идентификатора модели
    # model_id = await api.get_model()
    #
    # # Генерация изображения на основе модели и запроса
    # uuid = api.generate(prompt, model_id)
    #
    # # Проверка статуса генерации
    # images = await api.check_generation(uuid)
    #
    # # Сохранение изображения в файл
    save_image(images, path)


if __name__ == "__main__":
    prompt = "Гном был так увлечен изучением дома, что не заметил, как случайно разбил одну из ваз, стоявших на столе. Медведи были расстроены, потому что эта ваза была очень дорогой и красивой."
    path = "test2.png"
    asyncio.run(generate_image_new(prompt, path))
