import cv2
from Memory.short_term import ShortTermMemory
from Memory.long_term.long_term import LongTermMemory
from Processes.attention import AttentionController, TaskPriority
from Sensors.vision import VisionProcessor
from NeuralNet.pattern_recognition import ObjectRecognizer
from Processes.emotions import EmotionEngine
from Sensors.audio import AudioProcessor
from Processes.habits import HabitManager
from SystemUtils.voice import VoiceEngine
from NeuralNet.creativity import IdeaGenerator


class MindCore:
    def __init__(self):
        print("⚡ Ядро активировано")
        self.st_memory = ShortTermMemory()  # Инициализация памяти
        self.lt_memory = LongTermMemory("Memory/long_term/episodic.db")
        self.attention = AttentionController(self)
        self.vision = VisionProcessor()
        self.recognizer = ObjectRecognizer()
        self.emotion_engine = EmotionEngine()
        self.audio_processor = AudioProcessor()
        self.habit_manager = HabitManager(self)
        self.emotion_engine.emotion_intensity = 0.95
        self.voice_engine = VoiceEngine()
        self.idea_generator = IdeaGenerator()
        self._setup_sensors()
        self._load_modules()

    def _setup_sensors(self):
        """Инициализация сенсоров"""
        print("🎤 Аудиосенсор активирован")

    def _load_modules(self):
        """Загрузка критически важных модулей"""
        print("🌀 Загрузка памяти...")

        self.habit_manager.start()  # Запуск фонового мониторинга
        print("🔄 Загружены привычки")

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
        self._process_audio_input()

    def _run_diagnostics(self):
        """Тест работы памяти"""
        self.st_memory.add("Тестовый импульс")
        print(f"Тест памяти: {self.st_memory.recall()}")

        # Тест переключения фокуса
        current_task = self.attention.switch_focus()
        print(f"Текущий фокус: {current_task['id']}")

        """Тест работы камеры и распознавания объектов"""
        if not self.vision.camera:
            print("🚨 Камера не инициализирована!")
            return

        test_frame = self.vision.capture_frame()

        if test_frame is None:
            print("👁️ Визуальный сенсор: не удалось захватить кадр")
            return

        # Сохраняем сырой кадр
        cv2.imwrite("raw_camera_frame.jpg", test_frame)

        # Анализ объектов
        analysis = self.recognizer.analyze_frame(test_frame)
        print(f"🔍 Обнаружено: {analysis.get('count', 0)} объектов")

        # Визуализация результатов
        visualized = self.recognizer.visualize_detection(test_frame.copy(), analysis)
        cv2.imwrite("detection_result.jpg", visualized)


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

    def _process_audio_input(self):
        """Обработка аудиовхода и генерация ответа"""
        phrase = self.audio_processor.listen()
        if phrase:
            print(f"🎧 Распознано: {phrase}")
            # Генерация ответа
            response = self._generate_response(phrase)
            # Озвучивание
            emotion = self.emotion_engine.get_state()["emotion"]
            self.voice_engine.speak(response, emotion)

    def _generate_response(self, text: str) -> str:
        """Простой ИИ-ответ (заглушка)"""
        if "привет" in text.lower():
            return "Привет! Я вас слушаю."
        elif "как дела" in text.lower():
            return "Всё работает стабильно. Спасибо!"
        else:
            return "Повторите, пожалуйста."

    def shutdown(self):
        self.habit_manager.stop()  # Корректное завершение