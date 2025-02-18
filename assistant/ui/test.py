import torch
from silero import silero_tts

device = torch.device('cpu')  # Или 'cuda' для GPU
model, _ = silero_tts(language='ru', speaker='v3_1_ru')

# Генерация речи
audio = model.apply_tts(text="К сожалению я не могу говорить по английски", speaker='baya', sample_rate=48000)

# Сохранение аудио в файл
import soundfile as sf
sf.write("output.wav", audio.numpy(), samplerate=48000)
