import cv2
from Memory.short_term import ShortTermMemory
from Memory.long_term.long_term import LongTermMemory
from Processes.attention import AttentionController, TaskPriority
from Sensors.vision import VisionProcessor
from NeuralNet.pattern_recognition import ObjectRecognizer

class MindCore:
    def __init__(self):
        print("⚡ Ядро активировано")
        self.st_memory = ShortTermMemory()  # Инициализация памяти
        self.lt_memory = LongTermMemory("Memory/long_term/episodic.db")
        self.attention = AttentionController()
        self.vision = VisionProcessor()
        self.recognizer = ObjectRecognizer()
        self._load_modules()

    def _load_modules(self):
        """Загрузка критически важных модулей"""
        print("🌀 Загрузка памяти...")

    def boot(self):
        # Эмуляция первичных стимулов
        self.attention.add_task(
            task_id="system_init",
            priority=TaskPriority.CRITICAL,
            context={"source": "internal"}
        )
        print("✅ Сознание онлайн")
        self._run_diagnostics()
        self.simulate_environment()
        self.vision.live_preview()

    def _run_diagnostics(self):
        """Тест работы памяти"""
        self.st_memory.add("Тестовый импульс")
        print(f"Тест памяти: {self.st_memory.recall()}")

        # Тест переключения фокуса
        current_task = self.attention.switch_focus()
        print(f"Текущий фокус: {current_task['id']}")

        # Тест захвата кадра
        #test_frame = self.vision.capture_test_image("test_image.jpg")
        test_frame = self.vision.capture_frame()
        if test_frame is not None:
            # Сохраняем сырой кадр
            cv2.imwrite("raw_camera_frame.jpg", test_frame)

            # Анализ объектов
            analysis = self.recognizer.analyze_frame(test_frame)
            print(f"🔍 Обнаружено: {analysis.get('count', 0)} объектов")

            # Визуализация результатов
            visualized = self.recognizer.visualize_detection(test_frame.copy(), analysis)
            cv2.imwrite("detection_result.jpg", visualized)

        if test_frame is not None:
            analysis = self.recognizer.analyze_frame(test_frame)
            print(f"🔍 Обнаружено объектов: {analysis.get('count', 0)}")
            if "objects" in analysis:
                print("Список:", ", ".join(analysis["objects"]))

    def simulate_environment(self):
        """Имитация внешних стимулов"""
        # Добавляем задачи разного приоритета
        self.attention.add_task("fire_detected", TaskPriority.CRITICAL, {"sensor": "thermal"})
        self.attention.add_task("user_question", TaskPriority.HIGH, {"audio": "Привет, MindOS!"})
        self.attention.add_task("memory_cleanup", TaskPriority.LOW, {"type": "maintenance"})
        self.attention.add_task("visual_alert",TaskPriority.HIGH,{"type": "movement", "zone": "center"})

        # Обрабатываем задачи
        while True:
            task = self.attention.switch_focus()
            if not task:
                break
            print(f"[Фокус] {task['id']} ({task['priority'].name})")
            self.st_memory.add_task_context(task['id'], task['context'])