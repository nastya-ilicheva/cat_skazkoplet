from gtts import gTTS


def speach(text: str, test, filename='output1') -> str:
    if test:
        tts = gTTS(text=text,
                   lang='ru',
                   lang_check=False)
        tts.save(f'static/voice/{filename}.mp3')
        return f"voice/{filename}.mp3"
    pass





