import speech_recognition as sr # type: ignore
import sounddevice as sd # type: ignore
import numpy as np
import pyttsx3 # type: ignore
import wikipedia # type: ignore
import sys 

engine = pyttsx3.init()
engine.setProperty("rate", 170)   
engine.setProperty("volume", 1.0) 

def speak(text):
    print(f"Gini: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_user(duration=10):
     recognizer = sr.Recognizer() 
     sys.stdout.write("\a")
     sys.stdout.flush() 
     fs = 16000  
     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
     sd.wait()
     audio_data = sr.AudioData(recording.tobytes(), fs, 2)
     try:
        text = recognizer.recognize_google(audio_data)
        print(f"You: {text}")
        return text.lower()
     except sr.UnknownValueError:
        speak("Sorry, I did not catch that.")
        return ""
     except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""
def process_command(command):
    if"exit"in command:
        speak("Goodbye! see you soon.")
        exit()
    try:
       summary = wikipedia.summary(command, sentences=5)
       speak(summary)
    except wikipedia.DisambiguationError as e:
        speak(f"Your question is too broad. Did you mean {e.options[0]}?")
    except wikipedia.PageError:
        speak("Sorry, I could not find an answer for that.")
    except Exception:
        speak("I am not sure, but I will learn for next time.")
def main():
     speak("Hello, I am Gini. You can ask me anything.")
     while True:
        command = listen_user()
        if command:
            process_command(command)

if __name__ == "__main__":
    main()


