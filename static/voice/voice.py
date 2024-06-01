# https://github.com/snakers4/silero-models/
# V4
import os
import torch

import numpy as np

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'


if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)


sample_rate = 48000
# `speaker` should be in aidar, baya, kseniya, xenia, eugene, random
speaker = 'kseniya'


def speach(text: str, filename='output1') -> str:
    file_name = f'static/voice/{filename}.mp3'
    example_text = text
    audio_paths = model.save_wav(text=example_text,
                                 speaker=speaker,
                                 sample_rate=sample_rate)
    os.rename(audio_paths, file_name)
    return file_name