import numpy as np


def get_spectrum(signal):
    data_size = signal.size
    transformation = np.fft.fft(signal)
    freq = np.fft.fftfreq(data_size, d=1 / data_size)[0:data_size // 2]
    ampl = 2 / data_size * np.abs(transformation[0:data_size // 2])
    return freq, ampl
