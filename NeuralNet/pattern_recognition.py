import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np


class ObjectRecognizer:
    def __init__(self):
        self.model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        #self.model = models.detection.fasterrcnn_mobilenet_v3_large(pretrained=True)
        self.model.eval()  # Режим инференса
        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])
        self.classes = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
            'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign'
        ]  # Сокращенный список классов

        self.last_analysis = {}

    def update_analysis(self, frame):
        self.last_analysis = self.analyze_frame(frame)
        return self.last_analysis

    def analyze_frame(self, frame: np.ndarray) -> dict:
        """Анализ кадра и определение объектов"""
        try:
            # Конвертация OpenCV BGR -> RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            input_tensor = self.transform(pil_image).unsqueeze(0)

            with torch.no_grad():
                predictions = self.model(input_tensor)

            # Фильтрация результатов (порог уверенности 70%)
            scores = predictions[0]['scores'].numpy()
            high_confidence = scores > 0.7
            labels = [self.classes[i] for i in predictions[0]['labels'][high_confidence]]

            return {
                "objects": labels,
                "count": len(labels)
            }
        except Exception as e:
            return {"error": str(e)}