from gtts import gTTS
import os
from pydub import AudioSegment
from pydub import effects
import time


def speach(text: str, test, filename='output1') -> str:
    if not os.path.isfile(f'static/voice/{filename}.mp3'):
        if test:
            tts = gTTS(text=text,
                       lang='ru',
                       lang_check=False)
            tts.save(f'static/voice/{filename}.mp3')
            # while not os.path.isfile(f'static/voice/{filename}.mp3'):
            #     time.sleep(1)
            # audio = AudioSegment.from_mp3(f'static/voice/{filename}.mp3', )
            # a = audio.speedup(playback_speed=2.0)
            # a.export(f'static/voice/{filename}.mp3', format='mp3')
            return f"voice/{filename}.mp3"
    if os.path.isfile(f'static/voice/{filename}.mp3'):
        return f"voice/{filename}.mp3"


# if __name__ == "__main__":
#     speach('АААААААААААААААААААААА!', True, 'output12')
