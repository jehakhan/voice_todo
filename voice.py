import speech_recognition as sr
from utils import normalize_command

def listen_once():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Speak clearly...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        text = normalize_command(r.recognize_google(audio))
        print("Raw:", text)
        return str(text)
    except sr.UnknownValueError:
        print("Could not understand")
        return ""
    except sr.RequestError as e:
        print("API error:", e)
        return ""
