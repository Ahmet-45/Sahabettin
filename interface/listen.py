import speech_recognition as sr
import whisper


def listen_wake_word(wake_word="şahabettin"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 800
        print("Dinleniyor...")
        while True:
          audio = recognizer.listen(source)
          try:
              text = recognizer.recognize_whisper(audio, model="small", language="turkish").lower()
              print(f"Algılanan metin: {text}")
              if wake_word in text:
                  print("Wake word algılandı!")
                  return True
          except sr.UnknownValueError:
              print("Anlaşılamayan ses.")
    pass     

def record_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 800
        print("Komutunuzu söyleyin...")       
        try:
            audio = recognizer.listen(source, phrase_time_limit=5, timeout=5)
            text = recognizer.recognize_whisper(audio, model="small", language="turkish").lower()
            kelimeler = text.split()
            if len(kelimeler) < 2:  
                print("Çok kısa komut.")
                return None
            if "altyazı" in text or "abone" in text:
                print("Halüsinasyon tespit edildi, komut reddedildi.")
                return None
            
            print(f"Algılanan komut: {text}")
            return text
        except sr.UnknownValueError:
            print("Anlaşılamayan ses.")
        except sr.WaitTimeoutError:
            print("Zaman aşımı, komut alınamadı.")
            return None
    pass    
