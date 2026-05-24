import json
import os

class LongTermMemory:
    def __init__(self, filepath=os.path.join("storage", "sahabettin_memory.json")):
        self.filepath = filepath
        self.data = self._load_memory()

    def _load_memory(self):
      try:
          if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
          else:
            return {}
      except (json.JSONDecodeError, IOError) as e:
           print(f"Hafıza dosyası yüklenirken hata oluştu: {e}")
           return {}
      except Exception as e:
           print(f"Beklenmeyen bir hata oluştu: {e}")
           return {}
      

    def save_fact(self, key, value):
        self.data[key] = value
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Hafıza dosyasına yazılırken hata oluştu: {e}")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")
      

    def get_all_facts_for_prompt(self):
        if not self.data:
          return ""
        
        fact_list = []
                  
        for key, value in self.data.items():
          satir = f"{key}: {value}"
          fact_list.append(satir)

        return "\n".join(fact_list)               