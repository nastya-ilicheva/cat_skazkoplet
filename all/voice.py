# import speakerpy

VOICE_ID = 'rxEz5E7hIAPk7D3bXwf6'
CHUNK_SIZE = 1024
API_KEY_VOICE = '3f2fd6f1b6f41e9bd13d3aa26ca34f7b'
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY_VOICE
}


def speach(text: str, filename='output1', speed=1.5) -> str:
    data = {
        "text": text,
        'language': 'ru',
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            'speed': speed

        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(f'{filename}.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    return f'{filename}.mp3'
