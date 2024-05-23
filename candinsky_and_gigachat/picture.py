import replicate
import os
from translate import Translator
import time
import shutil
from PIL import Image
import requests

width = 480
height = 480
style = "картины акварелью"  # графика и аниме на выбор, картины Вангога
promt = 'мопс улыбается в новогоднем колпаке под ёлкой с подарками, тёплые тона, огоньки'

im_start_time = time.time()
os.environ["REPLICATE_API_TOKEN"] = "r8_ZJdXcugmNjCyo4viKDDrQpGbzmMjAdO2Nmsqc"


# MYGLOBAL = 0

def genirate_image(promt=promt, style="акварельные картины", width=480, height=480):
    promt = f'{promt}, стиль: {style}'
    transl = Translator(from_lang='ru', to_lang='en')
    promt = transl.translate(promt)
    print(promt)
    input = {
        "width": width,
        "height": height,
        "prompt": promt,
        "refine": "expert_ensemble_refiner",
        "apply_watermark": False,
        "num_inference_steps": 25
    }

    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input=input
    )
    im_finish_time = time.time()

    response = requests.get(*output, stream=True)
    print('время:', im_finish_time - im_start_time)

    with open('image.png', 'wb') as file:
        shutil.copyfileobj(response.raw, file)

    del response
    global MYGLOBAL
    # MYGLOBAL += 1
    image = 'image.png'

    return image

yet_gen = genirate_image('веселая корова жует травку на красной площади', 'инновационная сказка', 952,560)
img = Image.open(yet_gen)
img.save('im.png')
img.show()
# print(MYGLOBAL)