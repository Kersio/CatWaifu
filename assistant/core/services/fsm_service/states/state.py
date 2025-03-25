from assistant.core.services.fsm_service.context import Context


class State:

    def __init__(self, context: Context):
        self.context = context

    def process(self, user_input: str):
        """Обрабатывает ввод и возвращает следующее состояние"""

        raise NotImplementedError("Метод должен быть реализован в подклассе")

    def get_response(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
