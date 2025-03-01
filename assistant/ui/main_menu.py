import sys

from PySide6 import QtWidgets, QtGui, QtCore
from PIL import Image
from config import ICON_CHAT, ICON_SETTINGS, ICON_EXIT, CURRENT_AVATAR
from assistant.ui.strings import UI_STRINGS

MAIN_MENU_STRINGS = UI_STRINGS['main_menu']


class CustomButton(QtWidgets.QWidget):

    clicked = QtCore.Signal()  # Создаем сигнал clicked

    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)

        self.setFixedHeight(50)  # Высота кнопки

        # Создаем контейнер для кнопки
        self.container = QtWidgets.QWidget(self)
        self.container.setStyleSheet("""
            background-color: #FFB6C1;  /* Пастельный розовый */
            border-radius: 25px;        /* Скругление */
        """)
        self.container.setFixedSize(200, 50)  # Размер кнопки

        # Создаем белый круг
        self.circle = QtWidgets.QLabel(self.container)
        self.circle.setFixedSize(35, 35)  # Размер круга
        self.circle.setStyleSheet("""
            background-color: white;
            border-radius: 17px;         /* Круг */
            border: 2px solid #FF69B4;   /* Розовая граница */
        """)
        self.circle.move(8, 8)  # Размещаем круг в левой части контейнера

        # Устанавливаем иконку в круг
        self.icon = QtGui.QPixmap(icon_path).scaled(
            31, 31,  # Размер иконки
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.circle.setPixmap(self.icon)
        self.circle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Точный центр иконки

        # Создаем текстовую часть
        self.label = QtWidgets.QLabel(text, self.container)
        self.label.setStyleSheet("""
            color: white;              /* Белый текст */
            padding-left: 8px;         /* Отступ слева */
        """)
        self.label.setFont(QtGui.QFont("Comic Sans MS", 14))
        self.label.move(50, 0)  # Размещаем текст справа от круга
        self.label.setFixedSize(140, 50)  # Размер текстовой части
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)

        # Размещаем контейнер в QHBoxLayout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.setLayout(layout)

        # Добавляем флаг для отслеживания состояния наведения
        self.is_hovered = False

    def enterEvent(self, event):
        """Обработка входа курсора на кнопку"""
        self.is_hovered = True
        self.container.setStyleSheet("""
            background-color: #FF69B4;  /* Более насыщенный розовый */
            border-radius: 25px;
        """)
        self.circle.setStyleSheet("""
            background-color: #F0F0F0;  /* Сlightly darker background for the circle */
            border-radius: 17px;
            border: 2px solid #E91E63;  /* Darker border color */
        """)
        self.label.setFont(QtGui.QFont("Comic Sans MS", 16, QtGui.QFont.Weight.Bold))
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Обработка выхода курсора с кнопки"""
        self.is_hovered = False
        self.container.setStyleSheet("""
            background-color: #FFB6C1;  /* Пастельный розовый */
            border-radius: 25px;
        """)
        self.circle.setStyleSheet("""
            background-color: white;
            border-radius: 17px;
            border: 2px solid #FF69B4;  /* Original border color */
        """)
        self.label.setFont(QtGui.QFont("Comic Sans MS", 14))  # Размер шрифта
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        """Обработка события отпускания кнопки мыши"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()  # Отправляем сигнал при клике
        super().mouseReleaseEvent(event)


class ButtonsWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        # Создание кнопок
        buttons_strings = MAIN_MENU_STRINGS['buttons']
        self.chat_button = CustomButton(ICON_CHAT, buttons_strings["chat"], self)
        self.settings_button = CustomButton(ICON_SETTINGS, buttons_strings['settings'], self)
        self.exit_button = CustomButton(ICON_EXIT, buttons_strings['exit'], self)

        self.exit_button.clicked.connect(self.exit_event)

        # Размещение кнопок в QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.chat_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.exit_button)
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем небольшие отступы
        layout.setSpacing(10)  # Расстояние между кнопками
        self.setLayout(layout)
        # Скрываем окно по умолчанию
        self.hide()

    def exit_event(self):
        sys.exit()

    def set_position(self, x, y):
        """Устанавливает позицию окна"""
        self.move(x, y)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("CatWaifu")
        # Загрузка аватара
        avatar_path = CURRENT_AVATAR
        resized_pixmap = self.resize_image_with_pillow(avatar_path, (392, 416))
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
        self.buttons_window = ButtonsWindow(self)
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
            if self.buttons_window.isVisible():
                self.buttons_window.hide()
            elif not self.dragging:
                self.show_buttons_window()
        elif event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            # Скрываем кнопки при начале перемещения
            if self.buttons_window.isVisible():
                self.buttons_window.hide()

    def on_avatar_move(self, event):
        if self.dragging and self.offset:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            # Проверяем положение аватара на экране и отражаем его при необходимости
            self.update_avatar_reflection()
            # Обновляем позицию кнопок, если они видимы
            if self.buttons_window.isVisible():
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
            x = global_avatar_pos.x() - self.buttons_window.sizeHint().width() + offset
        y = global_avatar_pos.y() + (avatar_rect.height() - self.buttons_window.sizeHint().height()) // 2
        self.buttons_window.set_position(x, y)
        self.buttons_window.show()

    def update_buttons_position(self):
        """Обновляет позицию кнопок, если они видимы"""
        if self.buttons_window.isVisible():
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

    def resize_image_with_pillow(self, image_path, max_size):
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
