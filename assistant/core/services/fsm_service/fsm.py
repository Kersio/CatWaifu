import json
from fuzzywuzzy import process
import importlib

from assistant.core.services.fsm_service.context import Context
from config import (
    INITIAL_STATE_NAME,
    MINIMAL_SCORE,
    TEXT_FAILED_GET_STATE,
    STATES_PATH,
    FSM_CONFIG_PATH
)


class FSM:

    def __init__(self, config_path: str = FSM_CONFIG_PATH):
        self.context = Context()
        self.current_state = None
        self.config = self._load_config(config_path)
        self._register_commands()

    @staticmethod
    def _load_config(config_path: str) -> dict:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _register_commands(self):
        # Загружаем все команды из конфига
        commands = self.config["команды"]

        for cmd_name, cmd_data in commands.items():
            # Сохраняем ключевые слова и переходы
            setattr(self, f"_{cmd_name}_keywords", cmd_data["ключевые_слова"])
            setattr(self, f"_{cmd_name}_start_state", cmd_data["начальное_состояние"])
            setattr(self, f"_{cmd_name}_end_state", cmd_data["конечное_состояние"])

    def process(self, user_input):
        if self.current_state is None:
            self.current_state = self._get_initial_state()

        # Определяем текущее состояние через FuzzyWuzzy
        next_state_class = self._get_next_state(user_input)
        if next_state_class:
            self.current_state = next_state_class(self.context)
            return self.current_state.get_response()
        else:
            return TEXT_FAILED_GET_STATE

    def _get_next_state(self, user_input):
        # Ищем команду через FuzzyWuzzy
        for cmd_name in self.config["команды"]:
            keywords = getattr(self, f"_{cmd_name}_keywords")
            best_match, score = process.extractOne(user_input, keywords)
            if score > MINIMAL_SCORE:
                # Задаем следующее состояние из конфига
                next_state_name = self.config["команды"][cmd_name]["начальное_состояние"]
                return self._import_state_class(next_state_name)
        return None

    @staticmethod
    def _import_state_class(state_name: str):
        try:
            module = importlib.import_module(f"{STATES_PATH}.{state_name.lower()}_state")
            return getattr(module, state_name)

        except (ImportError, AttributeError):
            print(f"Ошибка: состояние '{state_name}' не найдено.")
            return None

    def _get_initial_state(self, initial_state: str = INITIAL_STATE_NAME):
        state_class = self._import_state_class(initial_state)
        return state_class(self.context)
