import librosa
import librosa.feature
import numpy as np
import matplotlib.pyplot as plt

# sample_rate is how many samples per second, e.g. 16000
# previously called DIVISOR, hop_length is how many samples we move forward per spectrogram frame
# therefore time per frame = hop_length / sample_rate --> with 16000 and 512 we get about 31.25 frames per second
# hop_length = 256 would be 2x more precise, but also much slower!

class AudioSource:
    sample_rate = 16000
    hop_length = 512
    n_mels = 512

    def __init__(self, path: str):
        self.path = path
        self.waveform, self.sample_rate_native = librosa.load(self.path, sr=self.sample_rate, mono=True)
        self.features = {}

    # These are equivalents: len(self.waveform), self.waveform.__len__(), self.waveform.shape[0]
    def sample_size(self):
        return len(self.waveform)

    # Returns the real time in seconds
    def duration(self):
        return self.sample_size() / self.sample_rate

    def get_mel_spectrogram(self, n_mels=n_mels):
        key = f"mel_{n_mels}"
        if key not in self.features:
            spectrogram = librosa.feature.melspectrogram(y=self.waveform, sr=self.sample_rate, n_mels=n_mels)
            self.features[key] = librosa.power_to_db(spectrogram, ref=np.max)
        return self.features[key]

class AudioView:
    def __init__(self, source: AudioSource, start: float, end: float):
        self.source = source
        self.start = max(0, start)
        self.end = min(end, source.duration())

    def duration(self):
        return self.end - self.start

    def sample_range(self):
        start_range = int(self.start * self.source.sample_rate)
        end_range = int(self.end * self.source.sample_rate)
        return start_range, end_range

    def get_waveform(self):
        start_range, end_range = self.sample_range()
        return self.source.waveform[start_range:end_range]

    def get_waveform_reverse(self):
        return self.get_waveform()[::-1]

    def get_mel_spectrogram(self, n_mels: int=AudioSource.n_mels):
        full = self.source.get_mel_spectrogram(n_mels)
        start_frame = int(self.start * self.source.sample_rate / self.source.hop_length)
        end_frame = int(self.end * self.source.sample_rate / self.source.hop_length)
        return full[:, start_frame:end_frame]

    def get_mel_spectrogram_reverse(self):
        return self.get_mel_spectrogram()[:, ::-1]

class Scope:
    def __init__(self, original: AudioSource, original_start: float, original_end: float):
        self.original = original
        self.start = max(0, original_start)
        self.end = min(original_end, original.duration())

    def duration(self):
        return self.end - self.start

    def get_view(self):
        return AudioView(self.original, self.start, self.end)

    def get_mel_spectrogram(self):
        return AudioView(self.original, self.start, self.end).get_mel_spectrogram()

    def print_status(self):
        print("\n--- SCOPE STATUS PRINT ---")
        print(f"Original Source-path: {self.original.path}")
        print(f"Original Start: {self.start}")
        print(f"Original End: {self.end}")
        print(f"Duration: {self.duration()}s")
        print(f"Duration: {self.duration()/60:.0f}m {self.duration()%60}s")
        print("--- SCOPE STATUS PRINT ---\n")

class Segment:
    def __init__(self, clip_view: AudioView, original_view: AudioView):
        self.clip = clip_view
        self.original = original_view

    def duration(self):
        return self.clip.duration()

    def print_status(self):
        print(f"Original Start: {self.original.start}")
        print(f"Original End: {self.original.end}")
        print(f"Clip Start: {self.clip.start}")
        print(f"Clip End: {self.clip.end}")
        print(f"Duration: {self.duration()}\n")

class Session:
    def __init__(self, original_path: str, clip_path: str):
        self.original_source = AudioSource(original_path)
        self.clip_source = AudioSource(clip_path)

        self.scope = None
        self.segments = []
        self.clip_cursor = 0.0

    def remaining_clip(self):
        return AudioView(self.clip_source, self.clip_cursor, self.clip_source.duration())

    def advance(self, seconds):
        self.clip_cursor += seconds

    def add_segment(self, clip_start, clip_end, original_start, original_end):
        segment = Segment(AudioView(self.clip_source, clip_start, clip_end), AudioView(self.original_source, original_start, original_end))
        self.segments.append(segment)

    def add_scope(self, original_start, original_end):
        self.scope = Scope(self.original_source, original_start, original_end)

    def print_status(self):
        self.scope.print_status()

        for i, segment in enumerate(self.segments):
            print(f"\nSegment {i+1}:")
            segment.print_status()