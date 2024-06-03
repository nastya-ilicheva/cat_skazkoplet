import numpy as np
import torch
import os

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
speaker = 'xenia'


def speach(text: str, test, filename='3_8') -> str:
    if not os.path.isfile(f'static/voice/{filename}.mp3'):
        if test:
            file_name = f'static/voice/{filename}.mp3'
            example_text = text
            audio_paths = model.save_wav(text=example_text,
                                         speaker=speaker,
                                         sample_rate=sample_rate)
            os.rename(audio_paths, file_name)
    return f"voice/{filename}.mp3"


if __name__ == "__main__":
    speach("'Конечно, вот полная сказка про таракана Томаса:"
           " Жил-был таракан по имени Томас. Он был обычным тараканом, "
           "но мечтал стать супергероем. Однажды, когда Томас сидел в своей норке и размышлял о жизни, "
           "он услышал громкий шум. Томас выбежал из своего убежища и увидел, что его дом разрушен. "
           "Все его друзья и соседи были в панике. Томас понял, что должен спасти всех. О"
           "н надел свой супергеройский костюм и взял свой супергеройский щит. "
           "Томас отправился на поиски злодея, который разрушил его дом. "
           "Он нашел его в подвале и начал сражение. Томас использовал свой супергеройский щит,"
           " чтобы отражать атаки злодея. В конце концов, Томас победил злодея и спас всех своих друзей и соседей. "
           "Он стал настоящим супергероем, и все его любили и уважали. "
           "Томас понял, что быть супергероем - это не только иметь суперспособности, но и иметь большое сердце и "
           "желание помочь другим. Томас продолжал жить своей жизнью супергероя. "
           "Он сражался со злом, защищал слабых и помогал всем, кто нуждался в помощи. "
           "Его друзья и соседи всегда были рядом, поддерживая его в трудные моменты. "
           "Томас стал настоящим примером для всех, кто хотел стать супергероем. "
           "Он доказал, что каждый может стать героем, если у него есть желание и стремление помочь другим.'", True)
