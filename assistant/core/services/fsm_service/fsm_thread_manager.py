import threading
import queue
from assistant.core.services.fsm_service.fsm import FSM
from assistant.core.services.audio_service import AudioService


class FSMThreadManager:
    def __init__(self, audio_service: AudioService):
        self.input_queue = queue.Queue()
        self.fsm = FSM(audio_service)
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_fsm, daemon=True)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def process_input(self, user_input):
        if not self.running:
            self.start()
        self.input_queue.put(user_input)

    def _run_fsm(self):
        while self.running:
            try:
                user_input = self.input_queue.get(timeout=1)
                response = self.fsm.process(user_input)
                print(f"FSM ответ: {response}")
            except queue.Empty:
                continue
