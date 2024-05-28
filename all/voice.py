import pyttsx3

def speach(text: str, filename='output1') -> str:
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.save_to_file(text, f"{filename}.mp3", )
    engine.runAndWait()
    return f"{filename}.mp3"

# speach("Привет", "output1")
# speach("Привет! Давай придумаем сказку вместе. Я буду задавать вопросы, а ты отвечать на них. Готов?", "output2")
