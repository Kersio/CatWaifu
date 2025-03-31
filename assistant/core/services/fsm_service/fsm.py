import json
from fuzzywuzzy import process
import importlib
from assistant.core.services.audio_service import AudioService
from assistant.core.services.fsm_service.states.WaitCommandState import WaitCommandState
from assistant.core.services.fsm_service.context import Context
from config import (
    INITIAL_STATE_NAME,
    MINIMAL_SCORE,
    TEXT_FAILED_GET_STATE,
    STATES_PATH,
    FSM_CONFIG_PATH
)


class FSM:

    def __init__(self, audio_service: AudioService, config_path: str = FSM_CONFIG_PATH):
        self.context = Context()
        self.context.data["audio_service"] = audio_service
        self.context.data["fsm"] = self
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
        # Если текущее состояние не задано, устанавливаем начальное состояние
        if self.current_state is None or type(self.current_state) is WaitCommandState:
            self.current_state = self._get_initial_state()

            # Проверяем, является ли user_input названием существующей команды
            next_state_class = self._get_next_state(user_input)
            if next_state_class:
                self.current_state = next_state_class(self.context)
                return
            else:
                return f"Ошибка: Не удалось импортировать конечное состояние для команды '{user_input}'."


        # Если текущее состояние уже задано
        else:
            # Проверяем, является ли user_input именем состояния
            if self._is_valid_state_name(user_input):
                next_state_class = self._import_state_class(user_input)
                if next_state_class:
                    self.current_state = next_state_class(self.context)
                    return
                else:
                    return "Ошибка: Не удалось импортировать состояние."

            # Если user_input не является именем состояния
            else:
                # Сохраняем user_input в контекст как context.data['temp']
                self.context.data['temp'] = user_input

                # Вызываем get_response у текущего состояния
                response = self.current_state.get_response()

                # Проверяем, является ли ответ именем следующего состояния
                if isinstance(response, str):
                    next_state_class = self._import_state_class(response)
                    if next_state_class:
                        self.current_state = next_state_class(self.context)
                        return self.current_state.get_response()
                    else:
                        return "Ошибка: Не удалось импортировать следующее состояние."
                else:
                    # Если ответ не является именем состояния, возвращаем его как результат
                    return response

    def _is_valid_state_name(self, state_name: str) -> bool:
        """
        Проверяет, является ли строка допустимым именем состояния.

        :param state_name: Строка для проверки.
        :return: True, если имя состояния допустимо, иначе False.
        """
        try:
            # Пытаемся импортировать состояние
            module = importlib.import_module(f"{STATES_PATH}.{state_name.lower()}_state")
            getattr(module, state_name)
            return True
        except (ImportError, AttributeError):
            return False

    def _handle_final_state(self, final_state_name):
        """Обработка конечного состояния."""
        print(f"Final state '{final_state_name}' reached.")
        # Выполняем действия для завершения задачи
        response = f"Задача завершена. Переход в начальное состояние."

        # Переходим в начальное состояние
        self.current_state = self._get_initial_state()
        return response

    def _get_next_state(self, user_input):
        # Ищем команду через FuzzyWuzzy
        for cmd_name in self.config["команды"]:
            keywords = getattr(self, f"_{cmd_name}_keywords")
            best_match, score = process.extractOne(user_input, keywords)
            if score > MINIMAL_SCORE:
                # Задаем следующее состояние из конфига
                next_state_name = self.config["команды"][cmd_name]["конечное_состояние"]
                return self._import_state_class(next_state_name)
        return None

    @staticmethod
    def _import_state_class(state_name: str):
        try:
            module = importlib.import_module(f"{STATES_PATH}.{state_name}")
            return getattr(module, state_name)

        except (ImportError, AttributeError):
            print(f"Ошибка: состояние '{state_name}' не найдено.")
            return None

    def _get_initial_state(self, initial_state: str = INITIAL_STATE_NAME):
        state_class = self._import_state_class(initial_state)
        return state_class(self.context)
