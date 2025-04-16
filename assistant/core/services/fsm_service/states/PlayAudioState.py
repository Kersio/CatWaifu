from assistant.core.services.fsm_service.states.state import State


class PlayAudioState(State):
    def process(self, user_input: str) -> str:
        audio_service = self.context.data.get("audio_service")
        if audio_service:
            audio_service.play_mp3(self.context.data['temp'])
        return "WaitCommandState"  # Возвращаемся в начальное состояние

    def get_response(self) -> str:
        return "Аудио воспроизводится..."
