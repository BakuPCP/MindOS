from typing import List, Dict
from enum import Enum

class TaskPriority(Enum):
    OBJECT_DETECTION = 3
    CRITICAL = 4    # Боль, опасность
    HIGH = 3        # Речь, визуальные стимулы
    MEDIUM = 2      # Фоновые процессы
    LOW = 1         # Воспоминания


class AttentionController:
    def __init__(self):
        self.active_tasks: List[Dict] = []
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
        """Переключить фокус на задачу с наивысшим приоритетом"""
        if not self.active_tasks:
            self.current_focus = None
            return

        # Выбор задачи по приоритету (FIFO для одинаковых приоритетов)
        self.active_tasks.sort(key=lambda x: x['priority'].value, reverse=True)
        self.current_focus = self.active_tasks.pop(0)
        return self.current_focus

    def _reprioritize(self):
        """Динамическое изменение приоритетов (заглушка для будущей логики)"""
        pass

    def get_current_focus(self):
        return self.current_focus