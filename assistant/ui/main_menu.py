import sys
from PIL import Image
from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Убираем заголовок окна и рамку
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool  # Делает окно "инструментальным" (исключает из Alt+Tab)
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Делает фон прозрачным

        # Настройка главного окна
        self.setWindowTitle("CatWaifu")

        # Загрузка и изменение размера изображения
        input_image_path = "avatar1.png"  # Путь к вашему изображению
        resized_pixmap = self.resize_image_with_pillow(input_image_path, (392, 416))

        # Создание QLabel для изображения
        self.avatar_label = QtWidgets.QLabel(self)
        self.avatar_label.setPixmap(resized_pixmap)  # Устанавливаем изменённое изображение
        self.avatar_label.setAlignment(QtCore.Qt.AlignCenter)  # Центрируем изображение
        self.avatar_label.mousePressEvent = self.on_avatar_click  # Обработчик клика
        self.avatar_label.mouseMoveEvent = self.on_avatar_move  # Обработчик перемещения
        self.avatar_label.mouseReleaseEvent = self.on_avatar_release  # Обработчик отпускания

        # Создание кнопок (изначально скрытых)
        self.button1 = QtWidgets.QPushButton("Кнопка 1", self)
        self.button2 = QtWidgets.QPushButton("Кнопка 2", self)
        self.button3 = QtWidgets.QPushButton("Кнопка 3", self)
        self.button4 = QtWidgets.QPushButton("Кнопка 4", self)

        # Скрываем кнопки
        self.hide_buttons()

        # Создаем контейнер для кнопок
        self.buttons_container = QtWidgets.QWidget(self)
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.addWidget(self.button1)
        self.buttons_layout.addWidget(self.button2)
        self.buttons_layout.addWidget(self.button3)
        self.buttons_layout.addWidget(self.button4)
        self.buttons_container.setLayout(self.buttons_layout)

        # Размещение элементов в горизонтальном layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.avatar_label)
        self.main_layout.addWidget(self.buttons_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Установка layout в центральный виджет
        container = QtWidgets.QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Устанавливаем размеры и позицию окна
        self.setGeometry(1475, 575, 392, 416)

        # Ат для перемещения окна
        self.dragging = False
        self.offset = None

    def on_avatar_click(self, event):
        """Обработчик клика на изображении"""
        if event.button() == QtCore.Qt.RightButton:  # Если нажата правая кнопка мыши
            if self.button1.isVisible():  # Если кнопки видны, скрываем их
                self.hide_buttons()
            else:
                self.show_buttons()  # Иначе показываем кнопки
        elif event.button() == QtCore.Qt.LeftButton:  # Если нажата левая кнопка мыши
            # Начинаем перемещение окна
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()  # Корректный offset

    def on_avatar_move(self, event):
        """Обработчик перемещения мыши"""
        if self.dragging and self.offset:
            # Вычисляем новую позицию окна
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)

    def on_avatar_release(self, event):
        """Обработчик отпускания мыши"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            self.offset = None

    def adjust_button_positions(self):
        """Корректирует положение кнопок"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()  # Размеры экрана
        window_geometry = self.geometry()  # Текущая позиция и размер окна

        # Определяем, находится ли окно в левой или правой части экрана
        is_left_half = window_geometry.center().x() < screen_geometry.width() / 2
        if is_left_half:
            # Если окно в левой половине экрана, кнопки размещаем справа
            self.main_layout.insertWidget(1, self.buttons_container)
        else:
            # Если окно в правой половине экрана, кнопки размещаем слева
            self.main_layout.insertWidget(0, self.buttons_container)

    def show_buttons(self):
        """Показывает кнопки"""
        self.adjust_button_positions()  # Корректируем положение кнопок
        self.button1.show()
        self.button2.show()
        self.button3.show()
        self.button4.show()

    def hide_buttons(self):
        """Скрывает кнопки"""
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()

    def resize_image_with_pillow(self, image_path, size):
        """
        Изменяет размер изображения с помощью Pillow.
        :param image_path: Путь к исходному изображению.
        :param size: Желаемый размер (ширина, высота).
        :return: QPixmap с изменённым изображением.
        """
        # Открываем изображение с помощью Pillow
        image = Image.open(image_path).convert("RGBA")  # Преобразуем изображение в RGBA (с прозрачностью)
        resized_image = image.resize(size, Image.Resampling.LANCZOS)  # Используем LANCZOS для масштабирования

        # Преобразуем Pillow Image в QPixmap
        qimage = QtGui.QImage(
            resized_image.tobytes(),  # Байты изображения
            resized_image.width,
            resized_image.height,
            resized_image.width * 4,  # bytesPerLine для RGBA (4 байта на пиксель)
            QtGui.QImage.Format_RGBA8888  # Формат изображения с прозрачностью
        )
        return QtGui.QPixmap.fromImage(qimage)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())