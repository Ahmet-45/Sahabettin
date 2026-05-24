from interface.listen import listen_wake_word, record_command
from core.brain import ask_llm
from interface.speak import speak_stream

def main():
  print("Şahabettin sistemi başlatıldı")

  while True:
    if listen_wake_word():
      
      while True:
        command = record_command()
        if command:
          print(f"Şahabettin düşünüyor: '{command}'")
          llm_response_generator = ask_llm(command)
          speak_stream(llm_response_generator)

          print("\nŞahabettin yanıt verdi. \n Şahabettin sizi tekrar dinlemeye başladı...")
        else:
          print("Sessizlik algılandı, uyku moduna geçiliyor...")
          break
if __name__ == "__main__":
    main()        
