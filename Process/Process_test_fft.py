import numpy as np
import matplotlib.pyplot as plt
import FFT.FFT as myfft
import Devices.Devices as dev


def simulate_sine(freq, amp):
    N = 10000
    T = 1.0 / 800

    omega = freq * 2.0 * np.pi
    x = np.linspace(0.0, N * T, N)
    y = amp * np.sin(omega * x)
    return y


oscilloscope = dev.Oscilloscope('123')
generator = dev.Generator('321')
freq, amp = myfft.get_spectrum(simulate_sine(2000, 3))
plt.plot(freq, amp)
plt.show()
