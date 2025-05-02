from enum import Enum
from typing import Dict

class EmotionType(Enum):
    JOY = "радость"
    FEAR = "страх"
    ANGER = "гнев"
    NEUTRAL = "нейтрально"

class EmotionEngine:
    def __init__(self):
        self.current_emotion = EmotionType.NEUTRAL
        self.emotion_intensity = 0.5  # 0.0 (мин) - 1.0 (макс)

    def evaluate_event(self, event_context: Dict) -> None:
        """Оценка события и генерация эмоции"""
        # Пример логики:
        if "risk_level" in event_context:
            risk = event_context["risk_level"]
            if risk > 0.7:
                self.current_emotion = EmotionType.FEAR
                self.emotion_intensity = max(0.8, risk)
            elif risk > 0.3:
                self.current_emotion = EmotionType.ANGER
                self.emotion_intensity = risk
        elif "social_interaction" in event_context:
            self.current_emotion = EmotionType.JOY
            self.emotion_intensity = 0.6

    def get_state(self) -> Dict:
        """Текущее эмоциональное состояние"""
        return {
            "emotion": self.current_emotion.value,
            "intensity": self.emotion_intensity
        }