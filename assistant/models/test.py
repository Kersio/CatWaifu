import sys
import time
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt

class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Загрузка...")
        self.setFixedSize(300, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Убираем рамку окна
        self.setAttribute(Qt.WA_TranslucentBackground)  # Прозрачный фон

        # Основной макет
        layout = QVBoxLayout()

        # Метка для отображения текста
        self.label = QLabel("Загрузка модели...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 16px;")

        # Добавляем метку в макет
        layout.addWidget(self.label)

        # Устанавливаем макет для окна
        self.setLayout(layout)

        # Таймер для имитации задачи
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.counter = 0

    def start_loading(self):
        """Запускает процесс загрузки."""
        self.show()  # Показываем окно
        self.timer.start(1000)  # Обновляем текст каждую секунду

    def update_text(self):
        """Обновляет текст на экране."""
        self.counter += 1
        if self.counter == 1:
            self.label.setText("Загрузка модели... Готово!")
        elif self.counter == 2:
            self.label.setText("Инициализация TTS...")
        elif self.counter == 3:
            self.label.setText("TTS готов к работе!")
            self.timer.stop()  # Останавливаем таймер
            self.close()  # Закрываем окно загрузки


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем и запускаем окно загрузки
    loading_window = LoadingWindow()
    loading_window.start_loading()

    sys.exit(app.exec())