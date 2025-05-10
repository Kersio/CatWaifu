from assistant.core.services.fsm_service.states.state import AwaitInputState
import subprocess


class OpenProgramState(AwaitInputState):
    PROGRAM_ALIASES = {
        "блокнот": "notepad.exe",
        "проводник": "explorer.exe",
        "командная строка": "cmd.exe",
    }

    def _on_input(self, user_input: str) -> str:
        program_name = self.PROGRAM_ALIASES.get(user_input, '')
        try:
            subprocess.Popen([program_name])
        except FileNotFoundError:
            print('Программа не найдена')
        return "WaitCommandState"

    def get_response(self) -> str:
        return 'Скажите название программы'
