import time
import threading
from typing import Dict, List
from enum import Enum

class HabitType(Enum):
    DAILY = "ежедневная"
    CONTEXTUAL = "контекстная"
    PROTECTIVE = "защитная"

class Habit:
    def __init__(self, name: str, habit_type: HabitType, action: callable, trigger: str = None):
        self.name = name
        self.type = habit_type
        self.action = action
        self.trigger = trigger  # Для контекстных привычек (например, "stress_level > 0.8")

class HabitManager:
    def __init__(self, mind_core):
        self.mind = mind_core
        self.habits: List[Habit] = []
        self._running = False
        self._thread = None

        # Инициализация базовых привычек
        self.add_habit(
            Habit(
                name="Автосохранение памяти",
                habit_type=HabitType.DAILY,
                action=lambda: (self.mind.lt_memory.save_state(),
                    print("[Автосохранение] Данные записаны")
                ),
            )
        )

        self.add_habit(
            Habit(
                name="Экстренное сохранение данных",
                habit_type=HabitType.PROTECTIVE,
                action=lambda: (
                    self.mind.lt_memory.force_save(),
                    print("⚠️ Экстренное сохранение!")
                ),
                trigger="emotion_intensity > 0.9"
            )
        )

    def add_habit(self, habit: Habit):
        self.habits.append(habit)

    def start(self):
        """Запуск фонового потока для привычек"""
        self._running = True
        self._thread = threading.Thread(target=self._monitor_habits)
        self._thread.start()

    def _monitor_habits(self):
        while self._running:
            # Проверка ежедневных привык каждые 10 секунд (для демо)
            time.sleep(10)
            for habit in self.habits:
                if habit.type == HabitType.DAILY:
                    habit.action()
                    print(f"[Привычка] {habit.name} выполнена")

            # TODO: Добавить проверку контекстных триггеров

    def stop(self):
        self._running = False
        self._thread.join()