from typing import List, Dict
from enum import Enum

class TaskPriority(Enum):
    OBJECT_DETECTION = 3
    CRITICAL = 4    # Боль, опасность
    HIGH = 3        # Речь, визуальные стимулы
    MEDIUM = 2      # Фоновые процессы
    LOW = 1         # Воспоминания
    SPEECH = 3


class AttentionController:
    def __init__(self, mind_core):
        self.mind = mind_core
        self.active_tasks = []
        self.current_focus = None

    def add_task(self, task_id: str, priority: TaskPriority, context: dict):
        """Добавить задачу в очередь внимания"""
        self.active_tasks.append({
            'id': task_id,
            'priority': priority,
            'context': context
        })
        self._reprioritize()

    def switch_focus(self):

        task = self.active_tasks.pop(0) if self.active_tasks else None
        if task:
            self.current_focus = task
            # Передаем контекст в эмоциональный движок
            self.mind.emotion_engine.evaluate_event(task["context"])
        return task

    def _reprioritize(self):
        """Динамическое изменение приоритетов (заглушка для будущей логики)"""
        pass

    def get_current_focus(self):
        return self.current_focus

    def handle_visual_input(self, objects: list):
        """Обработка визуальных стимулов"""
        if "person" in objects:
            self.add_task("human_detected", TaskPriority.HIGH, {"type": "social_interaction"})
        if "car" in objects:
            self.add_task("vehicle_nearby", TaskPriority.CRITICAL, {"risk_level": 0.8})