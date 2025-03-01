import os

# Базовый путь к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AVATARS_PATH = os.path.join(BASE_DIR, 'assets', 'avatars')
ICONS_PATH = os.path.join(BASE_DIR, 'assets', 'icons')

# Путь к конкретным аватарам
CURRENT_AVATAR = os.path.join(AVATARS_PATH, 'avatar1.png')
AVATAR_THINKING = os.path.join(AVATARS_PATH, 'think.png')

# Путь к изображениям кнопок, появляющихся при нажатии на аватар
ICON_CHAT = os.path.join(ICONS_PATH, 'chat.png')
ICON_SETTINGS = os.path.join(ICONS_PATH, 'settings.png')
ICON_EXIT = os.path.join(ICONS_PATH, 'exit.png')

ICON_CANCEL = os.path.join(ICONS_PATH, 'cancel.png')

# Параметры для TTS модели
LANGUAGE_TTS = 'ru'
SPEAKER_MODEL = 'v3_1_ru'
SPEAKER_VOICE = 'baya'
SAMPLE_RATE_TTS = 48000

