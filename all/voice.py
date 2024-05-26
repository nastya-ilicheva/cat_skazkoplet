# import webbrowser
# import requests
#
#
# def voice_acting(text: str, filename: str, lang='ru', speed=1.5, chunk_size=1024, voce_id='rxEz5E7hIAPk7D3bXwf6',
#                  api_key='3f2fd6f1b6f41e9bd13d3aa26ca34f7b') -> str:
#     VOICE_ID = voce_id
#     CHUNK_SIZE = chunk_size
#     API_KEY_VOICE = api_key
#     try:
#
#         url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
#
#         headers = {
#             "Accept": "audio/mpeg",
#             "Content-Type": "application/json",
#             "xi-api-key": API_KEY_VOICE
#         }
#
#         data = {
#             "text": text,
#             'language': lang,
#             "model_id": "eleven_multilingual_v2",
#             "voice_settings": {
#                 "stability": 0.5,
#                 "similarity_boost": 0.5,
#                 'speed': speed
#
#             }
#         }
#
#         response = requests.post(url, json=data, headers=headers)
#         with open(f'{filename}.mp3', 'wb') as f:
#             for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#                 if chunk:
#                     f.write(chunk)
#             f.close()
#         # webbrowser.open(f'{filename}.mp3')
#         return f'{filename}.mp3'
#
#     except Exception as e:
#         return str(e)
#
#
# if __name__ == '__main__':
#     text = '''Давай! Принцесса жила в большом замке со своей мамой и папой. Она была очень красивой и доброй девочкой. Однажды принцесса гуляла в саду и увидела большого дракона, который спал на камнях. Она подошла к нему и начала гладить его чешую. Дракон проснулся и увидел, что перед ним стоит маленькая девочка. Он был удивлен и испуган одновременно. Но принцесса не боялась дракона. Она знала, что драконы - это мифические существа, которые могут быть злыми или добрыми. Она решила, что этот дракон добрый, и решила подружиться с ним. Дракон был поражен смелостью и добротой принцессы. Он рассказал ей свою историю. Оказывается, он был изгнан из своего королевства за то, что отказался убивать людей. Теперь он жил один в горах и боялся, что его снова будут преследовать. Принцесса предложила дракону жить в ее замке. Она сказала ему, что он может быть ее другом и защитником. Дракон согласился и остался жить в замке. С тех пор принцесса и дракон стали лучшими друзьями. Они вместе играли, путешествовали и защищали друг друга от зла. И все были счастливы, потому что у них была такая замечательная дружба.'''
#     filename = 'сказка1'
#     voice_acting(text, filename)
import webbrowser
import requests

try:
    VOICE_ID = 'rxEz5E7hIAPk7D3bXwf6'
    CHUNK_SIZE = 1024
    API_KEY_VOICE = '3f2fd6f1b6f41e9bd13d3aa26ca34f7b'
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY_VOICE
    }

    data = {
        "text": "Путешествие в междумирье начинается, Ууууух!",
        'language': 'ru',
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            'speed': 1.5

        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output12.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    webbrowser.open('output12.mp3')

except Exception as e:
    print(e)
