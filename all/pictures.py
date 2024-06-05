import replicate
import os
import time

im_start_time = time.time()
os.environ["REPLICATE_API_TOKEN"] = "r8_HCzljf4wpJoRMRt3ivXroNxcVlujXTT18U9IK"


promt = 'bear as space commander'
input = {
    "width": 768,
    "height": 768,
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
a = ['https://replicate.delivery/pbxt/RO3yFZMbxTpQBtdLNXv9lWOCByd0GmGfupWvUJpBxraeA3ySA/out-0.png']
print(*a)


print('время:', im_finish_time - im_start_time)
