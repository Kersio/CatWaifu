from PySide6 import QtWidgets


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent):
        super().__init__(icon, parent)
        self.parent = parent  # Сохраняем ссылку на главное окно (AvatarWindow)
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

        # Добавление пункта "Скрыть аватар"
        self.hide_action = self.menu.addAction("Скрыть аватар")
        self.hide_action.triggered.connect(self.toggle_avatar_visibility)

        # Добавление пункта "Выход"
        exit_action = self.menu.addAction("Выход")
        exit_action.triggered.connect(self.exit_application)

        # Установка контекстного меню
        self.setContextMenu(self.menu)

    def toggle_avatar_visibility(self):
        """Переключение видимости аватара."""
        if self.parent.isVisible():
            self.parent.inactivity_timer.stop()
            self.parent.stop_listening()
            self.parent.hide()
            self.hide_action.setText("Показать аватар")  # Меняем текст кнопки
        else:
            self.parent.reset_inactivity_timer()
            self.parent.start_listening()
            self.parent.show()
            self.hide_action.setText("Скрыть аватар")  # Возвращаем исходный текст

    @staticmethod
    def exit_application():
        """Выход из приложения"""
        QtWidgets.QApplication.quit()
