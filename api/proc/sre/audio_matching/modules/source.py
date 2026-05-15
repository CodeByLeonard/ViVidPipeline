import librosa
import librosa.feature
import numpy as np

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

class Scope:
    def __init__(self, source: AudioSource, timestamps: list[dict]):
        self.source = source
        self.views = [ AudioView(source, timestamp["start"], timestamp["end"]) for timestamp in timestamps ]

    def scope_to_source_time(self, scope_time: float):
        current = 0.0
        for view in self.views:
            duration = view.duration()
            if current <= scope_time < current + duration:
                offset = scope_time - current
                return view.start + offset
            current += duration
        return None

    def duration(self):
        return sum(view.duration() for view in self.views)

    def get_waveform(self):
        waveforms = [view.get_waveform() for view in self.views]
        return np.concatenate(waveforms)

    def get_mel_spectrogram(self, n_mels: int = AudioSource.n_mels):
        spectrograms = [view.get_mel_spectrogram(n_mels) for view in self.views]
        return np.concatenate(spectrograms, axis=1)

class MatcherView:
    def __init__(self, source: AudioSource):
        self.source = source

    def get_waveform(self):
        return self.source.waveform[:]

    def get_mel_spectrogram(self, n_mels: int=AudioSource.n_mels):
        full = self.source.get_mel_spectrogram(n_mels)
        return full[:, :]

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

class SuperSegment:
    def __init__(self, segments):
        self.segments = segments

    def ignored_duration(self):
         return sum(
             segment.ignored_offset
             for segment in self.segments
         )

    def get_scope(self, source: AudioSource):
        timestamps = []
        for segment in self.segments:
            timestamps.append({"start": segment.start, "end": segment.end})
        return Scope(source, timestamps)

    def start(self):
        return self.segments[0].start

    def end(self):
        return self.segments[-1].end

    def duration(self):
        return self.end() - self.start()

    def corrected_duration(self):
        return self.duration() + self.ignored_duration()

    def print(self):
        print("\n--------- SEGMENT PRINT ---------")
        for index, segment in enumerate(self.segments):
            print(f"Index {index}: {segment.__str__()}")
        print("--------- SEGMENT PRINT ---------\n")