from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image


class ImageAnalyzer:
    def __init__(self, model_name: str = "google/vit-base-patch16-224"):

        self.feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
        self.model = ViTForImageClassification.from_pretrained(model_name)

    def describe_image(self, image_path: str) -> str:

        try:
            image = Image.open(image_path).convert("RGB")

            inputs = self.feature_extractor(images=image, return_tensors="pt")
            outputs = self.model(**inputs)

            predicted_class_idx = outputs.logits.argmax(-1).item()
            predicted_label = self.model.config.id2label[predicted_class_idx]
            return f"На изображении: {predicted_label}"
        except Exception as e:
            return f"Ошибка при анализе изображения: {str(e)}"
