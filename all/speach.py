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
speaker = 'baya'


def speach(text: str, filename='output1') -> str:
    file_name = f'static/voice/{filename}.mp3'
    example_text = text
    audio_paths = model.save_wav(text=example_text,
                                 speaker=speaker,
                                 sample_rate=sample_rate)
    os.rename(audio_paths, file_name)

speach('Выдры, облаченные в теплые гетры, бесшумно скользили по снегу, пробираясь сквозь сугробы к заветному месту. '
       'Их цель была ясна - кедры, полные вкусных орехов. Они быстро собирали их в свои ведра, не оставляя ни одного '
       'ядра без внимания. '
       'Но вдруг одна из выдр заметила что-то странное. Она остановилась и внимательно осмотрелась вокруг. '
       'Это было похоже на какой-то знак или предупреждение. Выдра решила, что лучше вернуться назад и сообщить об '
       'этом своим друзьям.', 'output11')

