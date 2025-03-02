import sys

from PySide6 import QtWidgets, QtGui, QtCore
from assistant.ui.avatar_window import AvatarWindow
from assistant.ui.system_tray import TrayIcon
from assistant.models.tts_model import TextToSpeechModel


def init_application():
    app = QtWidgets.QApplication([])

    # Создаем главное окно
    avatar_window = AvatarWindow()
    avatar_window.show()

    # Настройка трей-иконки
    icon_path = 'assets/icons/cat.png'
    pixmap = QtGui.QPixmap(icon_path).scaled(
        64, 64,
        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
    )
    icon = QtGui.QIcon(pixmap)
    tray_icon = TrayIcon(icon, avatar_window)
    tray_icon.show()

    return app, avatar_window, tray_icon


def run_application(app):
    sys.exit(app.exec())