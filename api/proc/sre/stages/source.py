from proc.sre.stages.parameters import load_params
from proc.sre.stages.session import get_session
from proc.sre.paths import SessionSRE
from pydantic import BaseModel
import librosa.feature
import numpy as np
import librosa
import json


class General(BaseModel):
    sample_rate: int
    hop_length: int
    n_mels: int

class Original(BaseModel):
    duration: float | None
    sample_size: float | None
    waveform_path: str=str(SessionSRE.SOURCE.ORIGINAL_WAVEFORM_NPY)
    mel_spectrogram_path: str=str(SessionSRE.SOURCE.ORIGINAL_MEL_NPY)

class Clip(BaseModel):
    duration: float | None
    sample_size: float | None
    waveform_path: str = str(SessionSRE.SOURCE.CLIP_WAVEFORM_NPY)
    mel_spectrogram_path: str = str(SessionSRE.SOURCE.CLIP_MEL_NPY)

class Scope(BaseModel):
    duration: float | None
    sample_size: float | None
    waveform_path: str = str(SessionSRE.SOURCE.SCOPE_WAVEFORM_NPY)
    mel_spectrogram_path: str = str(SessionSRE.SOURCE.SCOPE_MEL_NPY)

class SourceFile(BaseModel):
    general: General
    original: Original
    clip: Clip
    scope: Scope

SOURCE_FILEPATH = SessionSRE.SOURCE.SOURCE_JSON
def save_source(file: SourceFile):
    SOURCE_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SOURCE_FILEPATH, "w") as f:
        json.dump(file.model_dump(mode="json"), f, indent=2)

def load_source() -> SourceFile:
    if not SOURCE_FILEPATH.exists():
        raise FileNotFoundError("Matches does not exist")
    with open(SOURCE_FILEPATH, "r") as f:
        data = json.load(f)
    return SourceFile.model_validate(data)

def init_source_file():
    save_source(
        SourceFile(
            general=General(sample_rate=16000, hop_length=512, n_mels=512),
            original=Original(duration=None, sample_size=None),
            clip=Clip(duration=None, sample_size=None),
            scope=Scope(duration=None, sample_size=None),
        )
    )

def audio_source(path: str):
    source_file = load_source()
    sample_rate = source_file.general.sample_rate
    n_mels = source_file.general.n_mels
    hop_length = source_file.general.hop_length

    waveform, _ = librosa.load(path, sr=sample_rate, mono=True)

    sample_size = len(waveform)
    duration = sample_size / sample_rate

    mel_spectrogram_tmp = librosa.feature.melspectrogram(y=waveform, sr=sample_rate, n_mels=n_mels, hop_length=hop_length, center=False, n_fft=4096)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram_tmp, ref=np.max)

    return waveform, mel_spectrogram, sample_size, duration

def init_audio_source(source_path, waveform_path, mel_path, source_key: str):
    waveform, mel, sample_size, duration = audio_source(source_path)
    np.save(waveform_path, waveform)
    np.save(mel_path, mel)

    source_file = load_source()
    target = getattr(source_file, source_key)
    target.sample_size = sample_size
    target.duration = duration
    save_source(source_file)

def init_original_source():
    path = SessionSRE.EXTRACTION.ORIGINAL_MP3
    waveform_path = SessionSRE.SOURCE.ORIGINAL_WAVEFORM_NPY
    mel_path = SessionSRE.SOURCE.ORIGINAL_MEL_NPY
    source_key = "original"
    init_audio_source(path, waveform_path, mel_path, source_key)
    return

def init_clip_source():
    path = SessionSRE.EXTRACTION.CLIP_MP3
    waveform_path = SessionSRE.SOURCE.CLIP_WAVEFORM_NPY
    mel_path = SessionSRE.SOURCE.CLIP_MEL_NPY
    source_key = "clip"
    init_audio_source(path, waveform_path, mel_path, source_key)
    return

def init_scope_source():
    source_file = load_source()
    sample_rate = source_file.general.sample_rate
    hop_length = source_file.general.hop_length

    original_mel = np.load(SessionSRE.SOURCE.ORIGINAL_MEL_NPY)
    original_waveform = np.load(SessionSRE.SOURCE.ORIGINAL_WAVEFORM_NPY)

    scope_waveform_list = []
    scope_spectrogram_list = []
    for scope_segment in load_params().scopes:
        start_range = int(scope_segment.start * sample_rate)
        end_range = int(scope_segment.end * sample_rate)
        waveform = original_waveform[start_range:end_range]
        scope_waveform_list.append(waveform)

        start_frame = librosa.time_to_frames(scope_segment.start, sr=sample_rate, hop_length=hop_length)
        end_frame = librosa.time_to_frames(scope_segment.end, sr=sample_rate, hop_length=hop_length)
        mel = original_mel[:, int(start_frame):int(end_frame)]
        scope_spectrogram_list.append(mel)

    scope_waveform = np.concatenate(scope_waveform_list)
    scope_spectrogram = np.concatenate(scope_spectrogram_list, axis=1)

    np.save(SessionSRE.SOURCE.SCOPE_WAVEFORM_NPY, scope_waveform)
    np.save(SessionSRE.SOURCE.SCOPE_MEL_NPY, scope_spectrogram)

    source_file.scope.sample_size = len(scope_waveform)
    source_file.scope.duration = len(scope_waveform) / sample_rate
    save_source(source_file)
    return

def init_sources():
    init_original_source()
    init_clip_source()
    init_scope_source()

    import matplotlib.pyplot as plt
    original_mel = np.load(SessionSRE.SOURCE.ORIGINAL_MEL_NPY)
    clip_mel = np.load(SessionSRE.SOURCE.CLIP_MEL_NPY)
    scope_mel = np.load(SessionSRE.SOURCE.SCOPE_MEL_NPY)

    def plot_sources():
        plt.figure(figsize=(18, 10))

        plt.subplot(3, 1, 1)
        librosa.display.specshow(original_mel, sr=16000, x_axis="time", cmap="magma")
        plt.title("Original Mel Spectrogram")

        plt.subplot(3, 1, 2)
        librosa.display.specshow(clip_mel, sr=16000, x_axis="time", cmap="magma")
        plt.title("Clip Mel Spectrogram")

        plt.subplot(3, 1, 3)
        librosa.display.specshow(scope_mel, sr=16000, x_axis="time", cmap="magma")
        plt.title("Scope Mel Spectrogram")

        plt.show()
        plt.close()
        return

    # plot_sources()
    return