import os

# Базовый путь к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AVATARS_PATH = os.path.join(BASE_DIR, 'assets', 'avatars')
ICONS_PATH = os.path.join(BASE_DIR, 'assets', 'icons')

# Путь к конкретным аватарам
CURRENT_AVATAR = os.path.join(AVATARS_PATH, 'avatar1.png')
AVATAR_THINKING = os.path.join(AVATARS_PATH, 'think.png')

# Путь к изображениям кнопок, появляющихся при нажатии на аватар
ICON_CHAT = os.path.join(ICONS_PATH, 'chat2.png')
ICON_SETTINGS = os.path.join(ICONS_PATH, 'settings.png')
ICON_EXIT = os.path.join(ICONS_PATH, 'exit.png')

# Путь к изображению кнопки отмены
ICON_CANCEL = os.path.join(ICONS_PATH, 'cancel.png')

# Путь к изображению для иконки трея
ICON_TRAY = os.path.join(ICONS_PATH, 'cat.png')

# Параметры для TTS модели
LANGUAGE_TTS = 'ru'
SPEAKER_MODEL = 'v3_1_ru'
SPEAKER_VOICE = 'baya'
SAMPLE_RATE_TTS = 48000

# Знаки препинания для текста
PUNCTUATION_MARKS = ['.', ',', '?', '!']
FLAG_PUNCTUATION = True

# Текст приветствия при включении приложения
GREETING_TEXT = 'Привет, давно не виделись .'

# Параметры для аудио сервиса
SAMPLE_RATE_AUDIO = 53542

# Параметры для STT модели
MODEL_PATH_STT = os.path.join(BASE_DIR, 'assistant', 'models', 'vosk-model-small-ru-0.22')
SAMPLE_RATE_STT = 16000

# Параметры для FSM
INITIAL_STATE_NAME = 'wait_command'
MINIMAL_SCORE = 60
TEXT_FAILED_GET_STATE = 'Не поняла просьбу.'
STATES_PATH = os.path.join(BASE_DIR, 'assistant', 'core', 'services', 'fsm_services', 'states')
FSM_CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'fsm.json')
