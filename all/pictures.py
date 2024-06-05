import replicate
import os
from translate import Translator

os.environ["REPLICATE_API_TOKEN"] = "r8_Y1piYSDyvntnHRa8nZ0pQbEMoSvr8nT4MtM1r"


def translate_text(text):
    translator = Translator(from_lang="ru", to_lang="en")
    translation = translator.translate(text)
    return translation


def create_image(promt, width=512, height=512, num_pictures=1):
    promt = translate_text(promt) + ', in drawing style with clear contours and details'
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


print(create_image('милая девочка с куклой'))