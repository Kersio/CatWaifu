import os

# Базовый путь к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к аватарам
AVATARS_PATH = os.path.join(BASE_DIR, 'assets', 'avatars')

# Путь к конкретным аватарам
CURRENT_AVATAR = os.path.join(AVATARS_PATH, 'avatar1.png')
AVATAR_THINKING = os.path.join(AVATARS_PATH, 'think.png')