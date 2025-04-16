from assistant.core.init_app import init_application, run_application

if __name__ == "__main__":
    app = init_application()
    run_application(app)


# TODO: Проверку на русский язык в TTS модели
# TODO: обработчики ошибок в TTS модели
# TODO: переработать поток в audio_service
# TODO: Экран загрузки приложения
# TODO: фикс скрытия (STT_SERV(CE не создает новую модель STT)
# TODO: АБОБА
