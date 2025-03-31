from PySide6 import QtWidgets, QtGui, QtCore
from PIL import Image

from config import CURRENT_AVATAR, GREETING_TEXT
from assistant.ui.avatar_menu import AvatarMenu
from assistant.core.services.audio_service import AudioService
from assistant.core.services.fsm_service.fsm_thread_manager import FSMThreadManager
from assistant.core.services.stt_service import STTService


class AvatarWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.audio_service = AudioService()

        self.fsm_service = FSMThreadManager(self.audio_service)

        self.stt_service = STTService()
        self.stt_service.text_recognized_signal.connect(self.handle_recognized_text)

        self.is_greeting_played = False  # Флаг для отслеживания приветствия

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("CatWaifu")

        # Загрузка аватара
        avatar_path = CURRENT_AVATAR
        resized_pixmap = self.resize_image(avatar_path, (392, 416))

        # Создание QLabel для изображения
        self.avatar_label = QtWidgets.QLabel(self)
        self.avatar_label.setPixmap(resized_pixmap)
        self.avatar_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.mousePressEvent = self.on_avatar_click
        self.avatar_label.mouseMoveEvent = self.on_avatar_move
        self.avatar_label.mouseReleaseEvent = self.on_avatar_release

        # Устанавливаем фиксированный размер QLabel
        self.avatar_label.setFixedSize(resized_pixmap.size())

        # Создаем окно с кнопками
        self.avatar_menu = AvatarMenu(self)

        # Атрибуты для перемещения окна
        self.dragging = False
        self.offset = None
        self.is_reflected = False  # Флаг для отражения аватара
        # Сохраняем оригинальное изображение
        self.original_pixmap = resized_pixmap
        # Устанавливаем размеры и позицию окна
        self.setGeometry(1620, 635, 392, 416)

    def on_avatar_click(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.avatar_menu.isVisible():
                self.avatar_menu.hide()
            elif not self.dragging:
                self.show_buttons_window()
        elif event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            # Скрываем кнопки при начале перемещения
            if self.avatar_menu.isVisible():
                self.avatar_menu.hide()

    def on_avatar_move(self, event):
        if self.dragging and self.offset:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            # Проверяем положение аватара на экране и отражаем его при необходимости
            self.update_avatar_reflection()
            # Обновляем позицию кнопок, если они видимы
            if self.avatar_menu.isVisible():
                self.update_buttons_position()

    def on_avatar_release(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = False
            self.offset = None

    def show_buttons_window(self):
        avatar_rect = self.avatar_label.frameGeometry()
        global_avatar_pos = self.mapToGlobal(avatar_rect.topLeft())  # Глобальные координаты аватара

        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        is_left_half = (global_avatar_pos.x() + avatar_rect.width() // 2) < (screen_geometry.width() // 2)
        offset = 80
        if is_left_half:
            x = global_avatar_pos.x() + avatar_rect.width() - offset
        else:
            x = global_avatar_pos.x() - self.avatar_menu.sizeHint().width() + offset
        y = global_avatar_pos.y() + (avatar_rect.height() - self.avatar_menu.sizeHint().height()) // 2
        self.avatar_menu.set_position(x, y)
        self.avatar_menu.show()

    def update_buttons_position(self):
        """Обновляет позицию кнопок, если они видимы"""
        if self.avatar_menu.isVisible():
            self.show_buttons_window()

    def update_avatar_reflection(self):
        """Отражает аватар горизонтально в зависимости от его положения на экране"""
        avatar_rect = self.avatar_label.geometry()
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        is_left_half = (self.x() + avatar_rect.center().x()) < (screen_geometry.width() / 2)
        if is_left_half and not self.is_reflected:
            self.avatar_label.setPixmap(self.original_pixmap.transformed(QtGui.QTransform().scale(-1, 1)))
            self.is_reflected = True
        elif not is_left_half and self.is_reflected:
            self.avatar_label.setPixmap(self.original_pixmap)
            self.is_reflected = False

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        if not self.is_greeting_played:
            self.audio_service.sound_text(GREETING_TEXT)
            self.is_greeting_played = True

        self.start_listening()

    def handle_recognized_text(self, text: str):
        """Обработка распознанного текста."""
        print(f"Получен текст для FSM: {text}")
        # Передаем текст в FSM
        self.fsm_service.process_input(text)

    def start_listening(self) -> None:
        """Запуск STT-сервиса."""
        self.stt_service.start_listening()

    def stop_listening(self) -> None:
        """Остановка STT-сервиса."""
        self.stt_service.stop_listening()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Остановка сервисов при закрытии окна."""
        self.stop_listening()
        self.fsm_service.stop()
        super().closeEvent(event)


    @staticmethod
    def resize_image(image_path, max_size):
        # Открываем изображение и получаем его текущие размеры
        image = Image.open(image_path).convert("RGBA")
        original_width, original_height = image.size

        # Вычисляем коэффициенты масштабирования
        max_width, max_height = max_size
        width_ratio = max_width / original_width
        height_ratio = max_height / original_height

        # Берём минимальный из двух коэффициентов для сохранения пропорций
        scale_ratio = min(width_ratio, height_ratio)

        # Вычисляем новые размеры
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)

        # Масштабируем изображение с сохранением пропорций
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Конвертируем в QImage и затем в QPixmap
        qimage = QtGui.QImage(
            resized_image.tobytes(),
            resized_image.width,
            resized_image.height,
            resized_image.width * 4,
            QtGui.QImage.Format.Format_RGBA8888
        )
        return QtGui.QPixmap.fromImage(qimage)
