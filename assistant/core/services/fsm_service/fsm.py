import json
import importlib
from assistant.core.services.audio_service import AudioService
from assistant.core.services.fsm_service.context import Context
from config import (
    INITIAL_STATE_NAME,
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
        self.commands = self._parse_commands()
        self._state_cache = {}

    @staticmethod
    def _load_config(config_path: str) -> dict:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _parse_commands(self):
        commands = {}
        for cmd_name, cmd_data in self.config["commands"].items():
            commands[cmd_name] = {
                "keywords": cmd_data["keywords"],
                "end_state": cmd_data["end_state"],
            }
        return commands

    def process(self, user_input: str):
        if self.current_state is None:
            self.current_state = self._get_initial_state()

        next_state_name = self.current_state.process(user_input)
        if next_state_name:
            next_state_class = self._import_state_class(next_state_name)
            if next_state_class:
                self.current_state = next_state_class
            else:
                return f"Ошибка: состояние '{next_state_name}' не найдено"
        
        response = self.current_state.get_response()
        return response

    def _get_initial_state(self):
        return self._import_state_class(INITIAL_STATE_NAME)

    def _import_state_class(self, state_name: str):
        if state_name in self._state_cache:
            return self._state_cache[state_name]

        try:
            module = importlib.import_module(f"{STATES_PATH}.{state_name}")
            state_class = getattr(module, state_name)
            self._state_cache[state_name] = state_class(self.context)
            return self._state_cache[state_name]
        except (ImportError, AttributeError):
            return None
