import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write


def play_audio(audio_tensor, sample_rate):
    audio_numpy = audio_tensor.cpu().numpy()
    audio_numpy = audio_numpy / np.max(np.abs(audio_numpy))
    sd.play(audio_numpy, sample_rate)
    sd.wait()


def save_audio_to_file(audio_tensor, sample_rate, file_path="output.wav"):
    audio_numpy = audio_tensor.cpu().numpy()
    audio_numpy = (audio_numpy * 32767).astype(np.int16)  # Преобразование в 16-битный формат
    write(file_path, sample_rate, audio_numpy)
