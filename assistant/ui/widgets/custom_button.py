from PySide6 import QtWidgets, QtGui, QtCore


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
