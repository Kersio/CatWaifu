from assistant.core.init_app import init_application, run_application

if __name__ == "__main__":
    app, audio_service = init_application()
    audio_service.sound_text('Привет,. давно не виделись.')
    run_application(app)


# TODO: Проверку на русский язык в TTS модели
# TODO: Апгрейд TTS модели с помощью знаков препинания
# TODO: обработчики ошибок в TTS модели
