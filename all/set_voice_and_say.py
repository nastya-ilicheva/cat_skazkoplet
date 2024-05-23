import pyttsx3

tts = pyttsx3.init()

voices = tts.getProperty('voices')

# Задать голос по умолчанию

#tts.setProperty('voice', 'ru')

# Попробовать установить предпочтительный голос

for voice in voices:

    ru = voice.id.find('RHVoice\grandma')  # Найти Анну от RHVoice

    if ru > -1: # Eсли нашли, выбираем этот голос
        print(-1)

        tts.setProperty('voice', voice.id)

tts.say('Командный голос вырабатываю, товарищ генерал-полковник!')

tts.runAndWait()
