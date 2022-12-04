import datetime
import os.path

from FFT import FFT
from scipy import signal as sg

import numpy as np


class Device:
    def __init__(self, idn):
        self.identification = idn
        self.number_of_points = 1000
        self.usb_path = None
        self.data_read = None
        self.file = None

    def initialize(self):
        self.usb_path = '/dev/usbtmc0'
        while os.path.isfile(self.usb_path):
            if self.request('*IDN?', response=True, raw_data_file=False) and self.data_read == self.identification:
                return True
        return False

    def request(self, request_str, response=False, raw_data_file=True):
        with open(self.usb_path, 'rwb') as usbtmc:
            usbtmc.write(request_str)
            if response:
                self.data_read = usbtmc.read()
                if raw_data_file:
                    self.file = self.row_data_store('/../RowData/')
                return True
        return False

    @staticmethod
    def row_data_store(self, path, header='Header'):
        path = os.getcwd() + path
        file_name = str(datetime.datetime.now()) + '.txt'
        with open(os.path.join(path, file_name), 'w') as fp:
            fp.write(header)
            fp.write(self.data_read)
        return file_name

    def series(self, commands, output=False):
        for command in commands:
            response = (command[-1] == '?')
            self.request(command, response=response)
            if response:
                yield self.data_read
                if output:
                    print(self.data_read)


class Oscilloscope(Device):
    def __int__(self, idn):
        super().__init__(idn)
        self.commands = {}
        self.signal = [1, 2, 3]

    def get_spectrum(self, full_time, signal=None):
        if signal is None:
            x, signal = self.measure_signal(full_time)
            return FFT.get_spectrum(signal)
        return FFT.get_spectrum(signal)

    def shell(self, full_time, fft, wave_type):
        x, y = zip(*list(fft.items()))
        x, y = np.array(x), np.array(y)
        mask = list(*sg.argrelmax(y))
        return x[mask], y[mask]

    def analyse(self, full_time, shell, wave_type):
        x, y = zip(*list(shell.items()))
        x, y = np.array(x), np.array(y)
        mask = list(*sg.argrelmax(y))
        while len(mask) > 10:
            mask = list(*sg.argrelmax(y[mask]))
        return x[mask], y[mask]

    def measure_signal(self, full_time):
        return np.linspace(0, full_time, self.number_of_points), np.zeros(self.number_of_points)


class Generator(Device):
    def __init__(self, idn):
        super().__init__(idn)

    def __int__(self, idn):
        super().__init__(idn)
        self.signal = {'wave_type': '', 'freq': 0, 'amp': 0}
        self.reset()

    def reset(self):
        self.series(['*RST', 'C1:OUTP ON'])

    def set_wave(self, wave_type='SINE', freq=2000, amp=3):
        self.signal['wave_type'] = wave_type
        self.signal['freq'] = freq
        self.signal['amp'] = amp
        self.wave_to_gen()
        return self.simulate_wave(wave_type, freq, amp)

    def wave_to_gen(self):
        self.reset()
        wave_type = self.signal['wave_type']
        freq = self.signal['freq']
        amp = self.signal['amp']
        self.series(['C1:BSWV WVTP,' + wave_type, 'C1:BSWV FRQ,' + str(freq), 'C1:BSWV AMP,' + str(amp)])

    def simulate_wave(self, wave_type='SQUARE', freq=2000, freq2=200, amp=3, duty=0.05, full_time=1.):
        def rectangular(t, amp, freq, duty):
            return amp * (abs(t * freq) % 1 < duty) * (abs(t * freq2) % 1 < 0.05)

        def sine(t, amp, freq, duty):
            return amp * np.sin(2 * np.pi * freq * t) * (abs(t * freq) % 1 < duty) * (abs(t * freq2) % 1 < 0.05)

        omega = 2 * np.pi * freq
        x = np.linspace(0., full_time, self.number_of_points)

        if wave_type == 'SINE':
            signal = sine(x, amp, freq, duty)
            return x, signal
        if wave_type == 'SQUARE':
            signal = rectangular(x, amp, freq, duty)
            return x, signal
        if wave_type == 'MODULE':
            omega_0 = 10000
            m = 0.5
            return x, amp * m * np.cos(omega * x) * np.cos(omega_0 * x) + amp * np.cos(omega_0 * x)
