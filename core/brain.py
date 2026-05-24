import requests
import json
from storage.long_term_memory import LongTermMemory
from storage.short_term_memory import ShortTermMemory
from core.extractor import extract_fact_with_llm

uzun_sureli_hafiza = LongTermMemory()
kisa_sureli_hafiza = ShortTermMemory(max_size=5)
MAX_HAFIZA = 5

def ask_llm(user_prompt):

    if "kayda geçilsin" in user_prompt.lower():
        extracted_data = extract_fact_with_llm(user_prompt)
        if extracted_data:
            for key, value in extracted_data.items():
                uzun_sureli_hafiza.save_fact(key, value)

            yield "Bilgiyi kalıcı hafızaya başarıyla kaydettim efendiim."
        else:
            yield "Maalesef, bilgiyi kaydederken bir hata oluştu."
        return        
    

    url = "http://localhost:11434/api/generate"
    

    kalici_bilgiler = uzun_sureli_hafiza.get_all_facts_for_prompt()
    gecmis_metin = kisa_sureli_hafiza.get_history_as_string()

    akilli_prompt = f"""Sen Şahabettin adında zeki bir yapay zeka asistanısın. Kısa ve öz cevaplar verirsin. Kullanıcının sorusuna göre hareket eder ve ona yardımcı olmaya çalışırsın.
    Senin ve Kullanıcı hakkında bildiklerin: {kalici_bilgiler}   
    Önceki konuşmalar: {gecmis_metin}
    Kullanıcı: {user_prompt}
    Şahabettin:"""
    
    payload = {
        "model": "llama3",
        "prompt": akilli_prompt,
        "stream": True,
    }

    try:
        response = requests.post(url, json=payload, stream=True) # url'ye POST isteği gönderilir ve yanıt akış olarak alınır
        response.raise_for_status() # HTTP hatalarını kontrol eder
        tam_cevap = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                data = json.loads(decoded_line)
                if data.get("done"):                    
                    kisa_sureli_hafiza.add_dialogue(user_prompt, tam_cevap)
                    break
                kelime = data.get("response", "")
                tam_cevap += kelime
                yield kelime # Yanıtın "text" alanını döndürür
    except requests.exceptions.RequestException as e:
        print(f"HTTP isteği sırasında hata oluştu: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON çözümleme hatası: {e}")
        