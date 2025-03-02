import sys

from PySide6 import QtWidgets, QtCore
from config import ICON_CHAT, ICON_SETTINGS, ICON_EXIT
from assistant.ui.widgets.custom_button import CustomButton
from assistant.ui.strings import UI_STRINGS

AVATAR_MENU_STRINGS = UI_STRINGS['avatar_menu']


class AvatarMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        # Создание кнопок
        buttons_strings = AVATAR_MENU_STRINGS['buttons']
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

    @staticmethod
    def exit_event():
        sys.exit()

    def set_position(self, x, y):
        """Устанавливает позицию окна"""
        self.move(x, y)
