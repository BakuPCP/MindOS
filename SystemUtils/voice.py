import pyttsx3
from typing import Optional

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_engine()

    def _configure_engine(self):
        """Настройка параметров голоса"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Выбор голоса (0 - мужской, 1 - женский)
        self.engine.setProperty('rate', 150)  # Скорость речи (слов/мин)
        self.engine.setProperty('volume', 1.0)  # Громкость (0.0-1.0)

    def speak(self, text: str, emotion: Optional[str] = None):
        """Озвучивание текста с учетом эмоций"""
        if emotion:
            self._apply_emotion(emotion)
        self.engine.say(text)
        self.engine.runAndWait()
        self._reset_settings()

    def _apply_emotion(self, emotion: str):
        """Изменение голоса в зависимости от эмоции"""
        if emotion == "радость":
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 1.0)
        elif emotion == "гнев":
            self.engine.setProperty('rate', 200)
            self.engine.setProperty('volume', 0.9)
        elif emotion == "страх":
            self.engine.setProperty('rate', 130)
            self.engine.setProperty('volume', 0.6)

    def _reset_settings(self):
        """Сброс настроек к стандартным"""
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)