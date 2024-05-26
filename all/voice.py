import webbrowser
import requests

VOICE_ID = 'rxEz5E7hIAPk7D3bXwf6'
CHUNK_SIZE = 1024
API_KEY_VOICE = '3f2fd6f1b6f41e9bd13d3aa26ca34f7b'
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY_VOICE
}
def speach(s):

    data = {
        "text": s,
        'language': 'ru',
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            'speed': 1.5

        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output1.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    return 'output1.mp3'

webbrowser.open(speach('Привет'))

