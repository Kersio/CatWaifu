import sys
from PySide6 import QtWidgets, QtGui, QtCore
from assistant.ui.main_menu import MainWindow


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.setToolTip("CatWaifu")

        # Создание контекстного меню и сохранение его как атрибут класса
        self.menu = QtWidgets.QMenu()

        # Настройка стиля для меню (розовый фон)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #FFB6C1;  /* Пастельный розовый */
                border-radius: 8px;         /* Скругление углов */
            }
            QMenu::item {
                padding: 8px 32px;          /* Отступы для элементов */
                border-radius: 4px;         /* Скругление элементов */
            }
            QMenu::item:selected {
                background-color: #FF69B4;  /* Более насыщенный розовый при наведении */
                color: white;               /* Белый текст при наведении */
            }
        """)

        # Добавление пункта "Выход"
        exit_action = self.menu.addAction("Выход")  # Используем self.menu
        exit_action.triggered.connect(self.exit_application)

        # Установка контекстного меню
        self.setContextMenu(self.menu)

        # Обработка событий активации трей-иконки
        self.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        """Обработка событий активации трей-иконки"""
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            print("Трей-иконка была нажата")

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
    pixmap = QtGui.QPixmap(icon_path).scaled(
        64, 64,
        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
    )
    icon = QtGui.QIcon(pixmap)

    tray_icon = TrayIcon(icon, main_window)
    tray_icon.show()

    # Запускаем приложение
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

#TODO: Проверку на русский язык в TTS модели
#TODO: Апгрейд TTS модели с помощью знаков препинания
#TODO: обработчики ошибок в TTS модели