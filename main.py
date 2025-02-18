import sys
from PySide6 import QtWidgets, QtGui

from assistant.ui.main_menu import MainWindow

from config import ICON_CANCEL


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.setToolTip("CatWaifu")

        menu = QtWidgets.QMenu()

        exit_action = menu.addAction("Выход")
        exit_action.triggered.connect(self.exit_application)

        self.setContextMenu(menu)

        self.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        """Обработка событий активации трей-иконки"""
        pass

    def exit_application(self):
        """Выход из приложения"""
        QtWidgets.QApplication.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Создаем главное окно
    main_window = MainWindow()
    main_window.show()

    # Создаем трей-иконку
    icon_path = 'assets/icons/cat.png'
    pixmap = QtGui.QPixmap(icon_path).scaled(64, 64, QtGui.Qt.KeepAspectRatio, QtGui.Qt.SmoothTransformation)
    icon = QtGui.QIcon(pixmap)
    tray_icon = TrayIcon(icon, main_window)
    tray_icon.show()

    # Запускаем приложение
    sys.exit(app.exec())


if __name__ == "__main__":
    main()