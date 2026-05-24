import pyttsx3

engine = pyttsx3.init()

def speak_stream(llm_generator):
    """
    LLM'den gelen generator'ı (yield akışını) dinler ve cümle cümle okur.
    """
    buffer = ""
    for word in llm_generator:
        
        print(word, end='', flush=True)

        buffer += word

        if any(p in buffer for p in ['.',',','!','?']):
            engine.say(buffer)
            engine.runAndWait()

            buffer = ""    
        
    if len(buffer) > 0:
        engine.say(buffer)
        engine.runAndWait()