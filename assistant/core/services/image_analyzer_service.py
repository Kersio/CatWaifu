from concurrent.futures import ThreadPoolExecutor, Future
from assistant.models.image_analysis_model import ImageAnalyzer

class ImageService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.analyzer = ImageAnalyzer()

    def analyze_image(self, image_path: str) -> Future:
        return self.executor.submit(self.analyzer.describe_image, image_path)