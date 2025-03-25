import sys

from PySide6 import QtWidgets, QtGui, QtCore
from assistant.ui.avatar_window import AvatarWindow
from assistant.ui.system_tray import TrayIcon

def init_application():
    app = QtWidgets.QApplication([])

    # Создание аватара и запуск приветствия
    avatar_window = AvatarWindow()
    avatar_window.show()

    # Настройка трея
    icon_path = 'assets/icons/cat.png'
    pixmap = QtGui.QPixmap(icon_path).scaled(
        64, 64,
        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
    )
    icon = QtGui.QIcon(pixmap)
    tray_icon = TrayIcon(icon, avatar_window)
    tray_icon.show()

    def on_about_to_quit():
        avatar_window.audio_service.sound_text("До встречи!,")
        QtWidgets.QApplication.processEvents()
        avatar_window.audio_service.stop()

    app.aboutToQuit.connect(on_about_to_quit)

    return app


def run_application(app):
    sys.exit(app.exec())
