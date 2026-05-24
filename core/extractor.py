import requests
import json

def extract_fact_with_llm(user_input):
    """
    Kullanıcının cümlesinden JSON formatında veriyi çeker.
    Örnek Girdi: "Şahabettin kayda geçilsin, sevgilimin adı Tuğçe."
    Örnek Çıktı (JSON): {"sevgili_adi": "Tuğçe"}
    """
    url = "http://localhost:11434/api/generate"
    
    sistem_promptu = """
    Sen bir veri çıkarma yapay zekasısın. Girdiyi analiz et ve JSON dön.
    KURAL 1: Asla sohbet etme. Sadece geçerli JSON çıktısı ver.
    KURAL 2: Anahtar kelimeler arasında boşluk olmasın onun yerine alt çizgi olsun.
    KURAL 3: JSON degerine "kayda geçilsin" ifadesini ekleme
    """

    payload = {
        "model": "llama3",
        "prompt": f"{sistem_promptu}\n\nKullanıcı: {user_input}",
        "stream": False 
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() 

        ollama_paketi = response.json()
        llm_metni = ollama_paketi.get("response", "")
        ayristirilmis_veri = json.loads(llm_metni)
        
        return ayristirilmis_veri

    except requests.exceptions.RequestException as e:
        print(f"SİSTEM: Gizli Ajan sunucuya ulaşamadı! Hata: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"SİSTEM: Gizli Ajan düzgün JSON dönemedi (Gevezelik yaptı)! Hata: {e}")
        return None
    except Exception as e:
        print(f"SİSTEM: Beklenmeyen Ajan Hatası: {e}")
        return None