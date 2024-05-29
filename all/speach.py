import webbrowser
# import gtts
#
# tts = gtts.gTTS("Привет, я сказочник? чем я могу вам помочь?", lang="ru")
# tts.save("hello.mp3")
# playsound("hello.mp3")


# from gtts import gTTS
# import os
#
#
# def text_to_speech(text, lang='ru'):
#     tts = gTTS(text=text, lang=lang)
#     tts.save("output.mp3")
#     os.system("start output.mp3")
#
#
# text = "Привет, я сказочница, готовся мы сейчас будем портить тебе психику"
# text_to_speech(text)
#


import requests
try:
    VOICE_ID = 'Dvfxihpdb69LFIkmih0k'
    CHUNK_SIZE = 1024
    API_KEY_VOICE = '3f2fd6f1b6f41e9bd13d3aa26ca34f7b'
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": API_KEY_VOICE
    }

    data = {
      "text": "Привет, я сказочник, готовся мы сейчас будем портить тебе психику",
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('../voice/output1.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    webbrowser.open('../voice/output1.mp3')

except Exception as e:
    print(e)