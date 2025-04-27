import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights


class ObjectRecognizer:
    def __init__(self):
        self.threshold = 0.1

        self.model = models.detection.fasterrcnn_resnet50_fpn(
            weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        )
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
            if frame is None:
                return {"error": "Пустой кадр", "objects": [], "count": 0}

            # Конвертация BGR -> RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            input_tensor = self.transform(pil_image).unsqueeze(0)

            with torch.no_grad():
                raw_predictions = self.model(input_tensor)

            # Если нет обнаружений
            if len(raw_predictions) == 0 or 'boxes' not in raw_predictions[0]:
                return {"objects": [], "count": 0, "raw_predictions": raw_predictions}

            scores = raw_predictions[0]['scores'].cpu().numpy()
            mask = scores >= self.threshold
            labels = [self.classes[i] for i in raw_predictions[0]['labels'][mask].cpu().numpy()]

            return {
                "objects": labels,
                "count": len(labels),
                "raw_predictions": raw_predictions  # Для визуализации
            }
        except Exception as e:
            return {"error": str(e), "objects": [], "count": 0}

    def visualize_detection(self, frame: np.ndarray, analysis: dict) -> np.ndarray:
        """Отрисовка bounding boxes"""
        if "raw_predictions" not in analysis or len(analysis["raw_predictions"]) == 0:
            return frame

        try:
            predictions = analysis["raw_predictions"]
            boxes = predictions[0]['boxes'].cpu().numpy()
            labels = predictions[0]['labels'].cpu().numpy()
            scores = predictions[0]['scores'].cpu().numpy()

            for box, label, score in zip(boxes, labels, scores):
                if score < self.threshold:
                    continue

                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{self.classes[label]}: {score:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )
            return frame
        except Exception as e:
            print(f"🚨 Ошибка визуализации: {str(e)}")
            return frame