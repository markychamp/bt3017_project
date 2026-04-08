import numpy as np
from scipy.signal import stft


def generate_time_axis(sample_rate: int, duration: float) -> np.ndarray:
    """Generate a time axis for the audio signal."""
    return np.linspace(0, duration, int(sample_rate * duration), endpoint=False)


def generate_sine_wave(
    frequency: float,
    amplitude: float,
    sample_rate: int,
    duration: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a pure sine wave."""
    t = generate_time_axis(sample_rate, duration)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    return t, signal


def generate_mixed_tone(
    freq1: float,
    freq2: float,
    amp1: float,
    amp2: float,
    sample_rate: int,
    duration: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a signal made from two sine waves."""
    t = generate_time_axis(sample_rate, duration)
    signal = (
        amp1 * np.sin(2 * np.pi * freq1 * t)
        + amp2 * np.sin(2 * np.pi * freq2 * t)
    )
    return t, signal


def add_noise(signal: np.ndarray, noise_level: float, seed: int = 42) -> np.ndarray:
    """Add Gaussian noise to a signal."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, noise_level, size=len(signal))
    return signal + noise


def compute_fft(signal: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute FFT magnitude spectrum."""
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), d=1 / sample_rate)
    magnitude = np.abs(fft_vals)
    return freqs, magnitude


def compute_spectrogram(
    signal: np.ndarray,
    sample_rate: int,
    nperseg: int = 256,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute STFT-based spectrogram."""
    f, t, zxx = stft(signal, fs=sample_rate, nperseg=nperseg)
    magnitude = np.abs(zxx)
    return f, t, magnitude


def get_dominant_frequency(freqs: np.ndarray, magnitude: np.ndarray) -> float:
    """Return the dominant frequency from the FFT magnitude."""
    if len(freqs) == 0 or len(magnitude) == 0:
        return 0.0
    idx = np.argmax(magnitude)
    return float(freqs[idx])