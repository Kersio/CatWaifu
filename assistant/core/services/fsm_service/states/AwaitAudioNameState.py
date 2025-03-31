from .state import State
from config import AUDIO_PATH
from pathlib import Path


class AwaitAudioNameState(State):

    def get_response(self):
        user_input = self.context.data.get('temp', '')
        audio_service = self.context.data.get("audio_service")
        if not user_input:
            audio_service.sound_text('Не правильное имя файла для воспроизведени')
            return

        file_path = AUDIO_PATH + ('/'+user_input + '.mp3')
        path = Path(file_path)
        if path.exists() and path.is_file() and path.suffix.lower() == ".mp3":
            self.context.data['temp'] = file_path
            return self._proceed_to_play()
        else:
            audio_service.sound_text('Нет такого файла для воспроизведения')
            return

    @staticmethod
    def _proceed_to_play():
        return "PlayAudioState"  # Возвращаем имя следующего состояния