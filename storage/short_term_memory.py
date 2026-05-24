class ShortTermMemory:
    def __init__(self, max_size=5):
        self.history = []
        self.max_size = max_size

    def add_dialogue(self, user_text, assistant_text):
        self.history.append({"user": user_text, "assistant": assistant_text})
        # Sınırı aşarsa en eskisini at (Sliding Window)
        if len(self.history) > self.max_size:
            self.history.pop(0)

    def get_history_as_string(self):
        # Ajanın bahsettiği performans sorununu çözdük: List Comprehension + Join
        return "".join([f"Kullanıcı: {item['user']}\nŞahabettin: {item['assistant']}\n" for item in self.history])