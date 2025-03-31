from assistant.core.services.fsm_service.states.state import State
from assistant.core.services.fsm_service.context import Context


class PlayAudioState(State):
    def __init__(self, context: Context):
        super().__init__(context)

    def get_response(self):
        # Получаем audio_service из контекста
        audio_service = self.context.data.get("audio_service")
        if audio_service:
            audio_service.sound_text('Воспроизведение начато!')
            audio_service.play_mp3(self.context.data['temp'])
            return "WaitCommandState"
        else:
            return "WaitCommandState"
