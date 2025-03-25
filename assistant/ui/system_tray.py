from PySide6 import QtWidgets, QtGui, QtCore


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

    def exit_application(self):
        """Выход из приложения"""
        QtWidgets.QApplication.quit()
