from assistant.core.services.fsm_service.states.state import AwaitInputState
import subprocess


class CloseProgramState(AwaitInputState):
    PROGRAM_ALIASES = {
        "блокнот": "notepad.exe",
        "проводник": "explorer.exe",
        "командная строка": "cmd.exe",
    }

    def _on_input(self, user_input: str) -> str:
        program_name = self.PROGRAM_ALIASES.get(user_input, user_input.lower())

        try:
            subprocess.run(["taskkill", "/F", "/IM", program_name], check=True)
            response = f"Программа {program_name} успешно закрыта."
        except subprocess.CalledProcessError:
            response = f"Не удалось закрыть программу {program_name}. Возможно, она не запущена."

        print(response)
        return "WaitCommandState"

    def get_response(self) -> str:
        return 'Скажите название программы, которую нужно закрыть'
