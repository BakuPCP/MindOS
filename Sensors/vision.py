import cv2
import numpy as np
from typing import Optional

class VisionProcessor:
    def __init__(self):
        self.camera = None
        self.last_frame = None
        self._init_camera()

    def _init_camera(self):
        """Подключение к камере по умолчанию"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise RuntimeError("Камера не обнаружена")
        except Exception as e:
            print(f"🚨 Ошибка инициализации зрения: {str(e)}")

    def capture_frame(self) -> Optional[np.ndarray]:
        """Захват кадра в режиме реального времени"""
        if not self.camera or not self.camera.isOpened():
            return None

        ret, frame = self.camera.read()
        if ret:
            self.last_frame = frame
            return frame
        return None

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Препроцессинг изображения:
        - Конвертация в градации серого
        - Размытие для снижения шума
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        return blurred

    def release(self):
        """Освобождение ресурсов камеры"""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()

    def live_preview(self, duration_sec: int = 5):
        """Демо-режим захвата видео"""
        if not self.camera:
            return

        for _ in range(duration_sec * 30):  # 30 FPS
            frame = self.capture_frame()
            if frame is None:
                break

            processed = self.preprocess(frame)
            cv2.imshow("MindOS Vision Preview", processed)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release()

    #def load_test_image(self, path: str):
    #    """Для отладки без камеры"""
    #    self.last_frame = cv2.imread(path)
    #    return self.last_frame

    def capture_test_image(self):
        self.last_frame = cv2.imread("test_image.jpg")
        return self.last_frame