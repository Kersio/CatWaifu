import tkinter as tk
from tkinter import filedialog
from concurrent.futures import Future

from assistant.core.services.fsm_service.states.state import ImmediateActionState
from assistant.core.services.image_analyzer_service import ImageService


class DescribeImageState(ImmediateActionState):

    def _execute(self, user_input: str) -> str:
        image_service = ImageService()

        file_path = self._get_path()

        if not file_path:
            return "WaitCommandState"
        future: Future = image_service.analyze_image(file_path)
        description = future.result()

        self._on_image_described(description)
        return "WaitCommandState"

    def _get_path(self):
        root = tk.Tk()

        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        root.destroy()
        return file_path

    def _on_image_described(self, description: str):
        self.context.data["image_description"] = description
        print(self.context.data["image_description"])

    def get_response(self) -> str:
        return "Выберите изображение для анализа."
