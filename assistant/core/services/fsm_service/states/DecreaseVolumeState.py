import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from assistant.core.services.fsm_service.states.state import State


class DecreaseVolumeState(State):
    def process(self, user_input: str) -> str:
        # Получаем текущее устройство воспроизведения
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

        # Получаем текущий уровень громкости
        current_volume = volume.GetMasterVolumeLevelScalar()

        # Снижаем громкость на 10%
        new_volume = max(current_volume - 0.1, 0.0)  # Ограничиваем до 0%
        volume.SetMasterVolumeLevelScalar(new_volume, None)

        return "WaitCommandState"  # Возвращаемся в начальное состояние

    def get_response(self) -> str:
        return "Снижаю громкость..."
