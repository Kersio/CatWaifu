import json

from assistant.core.services.fsm_service.states.state import State
from config import FSM_CONFIG_PATH, MINIMAL_SCORE
from fuzzywuzzy import process


class WaitCommandState(State):
    def __init__(self, context):
        super().__init__(context)
        self.config = self._load_config(FSM_CONFIG_PATH)  # Загружаем конфиг команд

    @staticmethod
    def _load_config(config_path: str) -> dict:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def process(self, user_input: str) -> str:
        # Ищем команду через FuzzyWuzzy
        for cmd_name, cmd_data in self.config["commands"].items():
            keywords = cmd_data["keywords"]
            best_match, score = process.extractOne(user_input, keywords)
            if score > MINIMAL_SCORE:
                return cmd_data["end_state"]  # Возвращаем имя конечного состояния
        return ""  # Неопознанная команда

    def get_response(self) -> str:
        return "Жду команду."
