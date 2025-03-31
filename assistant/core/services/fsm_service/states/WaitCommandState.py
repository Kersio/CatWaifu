from .state import State


class WaitCommandState(State):

    def process(self, user_input):
        print('ожидание команды')

    def get_response(self):
        return "AwaitAudioNameState"