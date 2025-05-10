from assistant.core.services.fsm_service.context import Context


class State:

    def __init__(self, context: Context):
        self.context = context

    def process(self, user_input: str):
        """Обрабатывает ввод и возвращает следующее состояние"""

        raise NotImplementedError("Метод должен быть реализован в подклассе")

    def get_response(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")


class ImmediateActionState(State):
    def process(self, user_input: str) -> str:
        """Выполняет действие и возвращает следующее состояние."""
        return self._execute(user_input)

    def _execute(self, user_input: str) -> str:
        """
        Выполняет действие и возвращает имя следующего состояния.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError

    def get_response(self) -> str:
        return "Команда выполнена."
    
class AwaitInputState(State):
    def process(self, user_input: str) -> str:
        """Обрабатывает ввод и возвращает следующее состояние."""
        return self._on_input(user_input)

    def _on_input(self, user_input: str) -> str:
        """
        Обрабатывает пользовательский ввод.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError