from silero import silero_tts   
import torch

from config import LANGUAGE_TTS, SPEAKER_VOICE, SPEAKER_MODEL, SAMPLE_RATE_TTS, PUNCTUATION_MARKS, FLAG_PUNCTUATION

DEVICE = torch.device('cuda' if torch.cpu.is_available() else 'cpu')


class TextToSpeechModel:

    def __init__(self, lang: str = LANGUAGE_TTS, speaker_model: str = SPEAKER_MODEL) -> None:
        self.model = silero_tts(language=lang, speaker=speaker_model)[0]
        self.permissible_sample_rates = [8000, 24000, 48000]

    def generate_speech(self, text_of_speach: str, speaker_voice: str = SPEAKER_VOICE,
                        sample_rate: int = SAMPLE_RATE_TTS, put_accent: bool = True,
                        put_yo: bool = True) -> torch.Tensor:

        if not text_of_speach:
            text_of_speach = 'У меня пинг в голове.'

        if not (sample_rate in self.permissible_sample_rates):
            sample_rate = SAMPLE_RATE_TTS

        text_of_speach = self.process_text(text_of_speach) if FLAG_PUNCTUATION else text_of_speach

        return self.model.apply_tts(
            text=text_of_speach,
            speaker=speaker_voice,
            sample_rate=sample_rate,
            put_accent=put_accent,
            put_yo=put_yo
        )

    @staticmethod
    def process_text(text: str) -> str:
        for mark in PUNCTUATION_MARKS:
            text = text.replace(mark, mark+'.')
        return text
