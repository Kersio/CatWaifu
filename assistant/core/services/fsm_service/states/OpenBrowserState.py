import webbrowser
from assistant.core.services.fsm_service.states.state import AwaitInputState


class OpenBrowserState(AwaitInputState):
    def _on_input(self, user_input: str) -> str:
        # Формируем URL поиска Google
        search_query = user_input.strip().replace(" ", "+")
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)  # Открываем в браузере по умолчанию
        return "WaitCommandState"  # Возвращаемся в начальное состояние

    def get_response(self) -> str:
        return "Что именно найти в интернете?"
