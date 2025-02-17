from PIL import Image
from PyQt5 import QtWidgets, QtGui, QtCore


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
        self.button1 = QtWidgets.QPushButton("Кнопка 1", self)
        self.button2 = QtWidgets.QPushButton("Кнопка 2", self)
        self.button3 = QtWidgets.QPushButton("Кнопка 3", self)
        self.button4 = QtWidgets.QPushButton("Кнопка 4", self)

        # Размещение кнопок в QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
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
        input_image_path = "C:\\Users\\admin\\Desktop\\Papka\\FourSemester\\PPO\\CatWaifu\\assistant\\ui\\avatar1.png"
        resized_pixmap = self.resize_image_with_pillow(input_image_path, (392, 416))

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
