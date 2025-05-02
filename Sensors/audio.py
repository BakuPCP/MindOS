import speech_recognition as sr
from typing import Optional, Dict

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.last_phrase = ""

    def listen(self, timeout: int = 3) -> Optional[str]:
        """Запись аудио с микрофона"""
        with self.microphone as source:
            print("🔊 Прослушивание...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language="ru-RU")
                self.last_phrase = text
                return text
            except sr.WaitTimeoutError:
                return None
            except Exception as e:
                print(f"🚨 Ошибка распознавания: {str(e)}")
                return None

    def get_context(self) -> Dict:
        """Контекст для передачи в систему внимания"""
        return {"type": "speech", "content": self.last_phrase}