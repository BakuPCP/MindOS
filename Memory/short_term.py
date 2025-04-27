class ShortTermMemory:
    def __init__(self, capacity: int = 7):
        self.capacity = capacity  # Правило 7±2
        self.buffer = []

    def add(self, data: str):
        """Сохранить элемент, удаляя самый старый при переполнении"""
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append(data)

    def recall(self, n: int = None) -> list:
        """Воспроизвести последние n элементов (по умолчанию — все)"""
        return self.buffer[-n:] if n else self.buffer.copy()

    def flush(self):
        """Очистить буфер (например, перед сном)"""
        self.buffer.clear()

    def add_task_context(self, task_id: str, context: dict):
        self.add(f"TASK_{task_id}: {context}")