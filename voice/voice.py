import pyttsx3

def speach(text: str, filename='output1') -> str:
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.save_to_file(text, f"voice/{filename}.mp3", )
    engine.runAndWait()
    return f"voice/{filename}.mp3"


