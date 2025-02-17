from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image
from config import CURRENT_AVATAR
from assistant.ui.strings import UI_STRINGS

MAIN_MENU_STRINGS = UI_STRINGS['main_menu']

class CustomButton(QtWidgets.QWidget):
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)  # Фиксированная высота кнопки

        # Создаем контейнер для кнопки
        self.container = QtWidgets.QWidget(self)
        self.container.setStyleSheet("""
            background-color: #FFB6C1;  /* Пастельный розовый */
            border-radius: 20px;        /* Больше скругление */
        """)
        self.container.setFixedSize(200, 40)  # Размер кнопки

        # Создаем белый круг
        self.circle = QtWidgets.QLabel(self.container)
        self.circle.setFixedSize(30, 30)  # Размер круга
        self.circle.setStyleSheet("""
            background-color: white;
            border-radius: 15px;         /* Круг */
            border: 2px solid #FF69B4;   /* Розовая граница */
        """)
        self.circle.move(5, 5)  # Размещаем круг в левой части контейнера

        # Устанавливаем иконку в круг
        self.icon = QtGui.QPixmap(icon_path).scaled(24, 24, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.circle.setPixmap(self.icon)
        self.circle.setAlignment(QtCore.Qt.AlignCenter)

        # Создаем текстовую часть
        self.label = QtWidgets.QLabel(text, self.container)
        self.label.setStyleSheet("""
            color: white;              /* Белый текст */
            font-size: 14px;           /* Размер шрифта */
            padding-left: 10px;        /* Отступ слева */
        """)
        self.label.move(45, 0)  # Размещаем текст справа от круга
        self.label.setFixedSize(150, 40)  # Размер текстовой части
        self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        # Размещаем контейнер в QHBoxLayout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.setLayout(layout)

    def mousePressEvent(self, event):
        """Обработка нажатия на кнопку"""
        if event.button() == QtCore.Qt.LeftButton:
            print(f"Clicked: {self.label.text()}")


class ButtonsWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Создание кнопок
        buttons_strings = MAIN_MENU_STRINGS['buttons']
        self.button1 = CustomButton("icons/settings.png", buttons_strings['settings'], self)
        self.button2 = CustomButton("icons/exit.png", buttons_strings['exit'], self)
        self.button3 = CustomButton("icons/chat.png", buttons_strings["chat"], self)

        # Размещение кнопок в QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем небольшие отступы
        layout.setSpacing(10)  # Расстояние между кнопками
        self.setLayout(layout)

        # Скрываем окно по умолчанию
        self.hide()

    def set_position(self, x, y):
        """Устанавливает позицию окна"""
        self.move(x, y)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("CatWaifu")

        # Загрузка аватара
        avatar_path = CURRENT_AVATAR
        resized_pixmap = self.resize_image_with_pillow(avatar_path, (392, 416))

        # Создание QLabel для изображения
        self.avatar_label = QtWidgets.QLabel(self)
        self.avatar_label.setPixmap(resized_pixmap)
        self.avatar_label.setAlignment(QtCore.Qt.AlignCenter)
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
        if event.button() == QtCore.Qt.RightButton:
            if self.buttons_window.isVisible():
                self.buttons_window.hide()
            elif not self.dragging:
                self.show_buttons_window()
        elif event.button() == QtCore.Qt.LeftButton:
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
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            self.offset = None

    def show_buttons_window(self):
        avatar_rect = self.avatar_label.geometry()
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()

        # Определяем, находится ли аватар в левой или правой части экрана
        is_left_half = (self.x() + avatar_rect.center().x()) < (screen_geometry.width() / 2)

        # Уменьшаем отступ до 5 пикселей
        offset = 5
        if is_left_half:
            # Если аватар в левой части экрана, показываем кнопки справа
            x = avatar_rect.right() + offset
        else:
            # Если аватар в правой части экрана, показываем кнопки слева
            x = avatar_rect.left() - self.buttons_window.width() - offset

        # Вычисляем вертикальную позицию для центрирования кнопок
        y = avatar_rect.top() + (avatar_rect.height() - self.buttons_window.height()) // 2

        # Устанавливаем позицию окна с кнопками
        self.buttons_window.set_position(self.x() + x, self.y() + y)
        self.buttons_window.show()

    def update_buttons_position(self):
        if self.buttons_window.isVisible():
            self.show_buttons_window()

    def update_avatar_reflection(self):
        """Отражает аватара горизонтально в зависимости от его положения на экране"""
        avatar_rect = self.avatar_label.geometry()
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()

        # Определяем, находится ли аватар в левой или правой части экрана
        is_left_half = (self.x() + avatar_rect.center().x()) < (screen_geometry.width() / 2)

        # Если аватар в левой части экрана и не отражен — отражаем его
        if is_left_half and not self.is_reflected:
            self.avatar_label.setPixmap(self.original_pixmap.transformed(QtGui.QTransform().scale(-1, 1)))
            self.is_reflected = True
        # Если аватар в правой части экрана и отражен — возвращаем его в исходное состояние
        elif not is_left_half and self.is_reflected:
            self.avatar_label.setPixmap(self.original_pixmap)
            self.is_reflected = False

    def resize_image_with_pillow(self, image_path, size):
        image = Image.open(image_path).convert("RGBA")
        resized_image = image.resize(size, Image.Resampling.LANCZOS)
        qimage = QtGui.QImage(
            resized_image.tobytes(),
            resized_image.width,
            resized_image.height,
            resized_image.width * 4,
            QtGui.QImage.Format_RGBA8888
        )
        return QtGui.QPixmap.fromImage(qimage)