from assistant.core.services.fsm_service.states.state import AwaitInputState
from config import AUDIO_PATH
from pathlib import Path


class AwaitAudioNameState(AwaitInputState):
    def _on_input(self, user_input: str) -> str:
        file_path = Path(AUDIO_PATH) / f"{user_input}.mp3"
        if file_path.exists() and file_path.suffix.lower() == ".mp3":
            self.context.data['temp'] = str(file_path)
            return "PlayAudioState"  # Переход к воспроизведению
        else:
            return ""  # Файл не найден

    def get_response(self) -> str:
        return "Введите название аудиофайла:"
