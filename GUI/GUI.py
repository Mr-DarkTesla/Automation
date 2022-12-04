import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

from Devices import Devices

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.online = {}
        self.panel = None
        self.menu = None
        self.axes = None
        self.change_button = None
        self.plot_entry_amp = None
        self.plot_entry_freq = None
        self.change_wave_type = None
        self.module = None
        self.square = None
        self.sine = None
        self.plot_button = None
        self.figure_canvas = None
        self.figure = None
        self.subplot_format = None
        self.signal = None
        self.full_time = None
        self.oscilloscope = None
        self.generator = None

        self.set_constants()
        self.set_window_params()

        self.set_layout()

    def plot_signal(self):
        def adjast_obj(obj):
            if len(obj) == 0:
                return {0: 0}
            return obj

        timeunits, simulated = self.generator.simulate_wave(wave_type=self.signal['wave_type'],
                                                            freq=self.signal['freq'], amp=self.signal['amp'],
                                                            duty=self.signal['duty'],
                                                            full_time=self.full_time)
        obj_sim_sig = dict(zip(timeunits, simulated))

        freq, amp = self.oscilloscope.get_spectrum(self.full_time, signal=simulated)
        freq /= self.full_time
        obj_sim_fft = adjast_obj(dict(zip(freq, amp)))

        x, y = self.oscilloscope.shell(self.full_time, obj_sim_fft, self.signal['wave_type'])
        obj_sim_shell = adjast_obj(dict(zip(x, y)))

        # x, y = self.oscilloscope.analyse(self.full_time, obj_sim_shell, self.signal['wave_type'])
        # obj_sim_shell_of_shell = dict(zip(1. / x, y))

        timeunits, measured = self.oscilloscope.measure_signal(self.full_time)
        obj_mes_sig = adjast_obj(dict(zip(timeunits, measured)))

        freq, amp = self.oscilloscope.get_spectrum(self.full_time)
        freq /= self.full_time
        obj_mes_fft = adjast_obj(dict(zip(freq, amp)))

        x, y = self.oscilloscope.shell(self.full_time, obj_mes_fft, self.signal['wave_type'])
        obj_mes_shell = adjast_obj(dict(zip(x, y)))

        # x, y = self.oscilloscope.analyse(self.full_time, obj_mes_shell, self.signal['wave_type'])
        # obj_mes_shell_of_shell = dict(zip(1. / x, y))

        self.plot_graph([obj_sim_sig, obj_mes_sig], 1, fmt=['r-', 'b-'], labels=['Simulated', 'Measured'],
                        label_x=r't, s',
                        label_y=r'A, V', title='Signal')

        self.plot_graph([obj_sim_fft, obj_mes_fft], 2, fmt=['r-', 'b-'], labels=['Simulated', 'Measured'],
                        label_x=r'$\omega$, Hz',
                        label_y=r'A, V', title='FFT')

        self.plot_graph([obj_sim_shell, obj_mes_shell], 3, fmt=['r.', 'b.'], labels=['Simulated', 'Measured'],
                        label_x=r'$\omega$, Hz',
                        label_y=r'A, V', title='Shell')

        # self.plot_graph([obj_sim_shell_of_shell, obj_mes_shell_of_shell], 4, fmt=['r.', 'b.'], labels=['Simulated', 'Measured'],
        #                 label_x=r'$\frac{1}{\omega}$, Hz^{-1}',
        #                 label_y=r'A, V', title='')

        date = str(datetime.datetime.now())
        plt.savefig('RawData/{}.svg'.format('graph--' + date + '--' + self.signal['wave_type']), format='svg', dpi=100)
        file_name = '{}.svg'.format('objects--' + date + '--' + self.signal['wave_type'])
        with open(os.path.join('RawData/', file_name), 'w') as fp:
            print(obj_sim_sig, file=fp)
            print(obj_sim_fft, file=fp)
            print(obj_sim_shell, file=fp)
            print(obj_mes_sig, file=fp)
            print(obj_mes_fft, file=fp)
            print(obj_mes_shell, file=fp)

    def plot_graph(self, data, subplot, fmt=None, labels=None, label_x='', label_y='', title=''):
        if labels is None:
            labels = ['']
        if fmt is None:
            fmt = ['r.']
        subplot = int(str(self.subplot_format) + str(subplot))
        sub_fig = self.figure.add_subplot(subplot)
        for array, format, label in zip(data, fmt, labels):
            lists = sorted(array.items())  # sorted by key, return a list of tuples
            x, y = zip(*lists)  # unpack a list of pairs into two tuples
            sub_fig.plot(x, y, format, label=label)

        sub_fig.set_xlabel(label_x)
        sub_fig.set_ylabel(label_y)
        sub_fig.set_title(title)
        sub_fig.grid(True, which='both')
        sub_fig.axhline(y=0, color='k')
        sub_fig.axvline(x=0, color='k')
        sub_fig.legend()

    def set_constants(self):
        self.generator = Devices.Generator('123')
        self.oscilloscope = Devices.Oscilloscope('321')
        self.online["generator"] = self.generator.initialize()
        self.online["oscilloscope"] = self.oscilloscope.initialize()
        self.full_time = 1.
        self.signal = {'wave_type': 'SQUARE', 'freq': 8000, "amp": 3}

    def set_window_params(self):
        self.geometry("1000x1000+10+10")
        self.title('Fourie Automation')
        self.figure = Figure(dpi=100)
        self.figure.subplots_adjust(hspace=0.7)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.subplot_format = 31
        self.axes = []

    def set_layout(self):
        self.change_wave_type = tk.StringVar()
        self.change_wave_type.set('')

        self.panel = tk.Frame()
        self.panel.pack(side=tk.TOP)

        self.menu = tk.Frame(self.panel)
        self.menu.pack(side=tk.LEFT, padx=10)

        self.sine = tk.Radiobutton(self.menu, text="SINE",
                                   variable=self.change_wave_type, value='SINE')
        self.square = tk.Radiobutton(self.menu, text="SQUARE",
                                     variable=self.change_wave_type, value='SQUARE')
        self.module = tk.Radiobutton(self.menu, text="MODULE",
                                     variable=self.change_wave_type, value='MODULE')

        self.sine.pack()
        self.square.pack()
        self.module.pack()

        self.plot_entry_freq = tk.Entry(self.panel, width=30)
        self.plot_entry_freq.insert(0, "20 3 0.25")
        self.plot_entry_freq.pack()

        self.change_button = tk.Button(self.panel, text="Change",
                                       command=self.change_wave)
        self.change_button.pack()

        # create the toolbar
        NavigationToolbar2Tk(self.figure_canvas, self)

    def change_wave(self):
        self.signal['wave_type'] = self.change_wave_type.get()
        freq = self.plot_entry_freq.get()
        try:
            list_input = list(map(float, freq.split()))
            self.signal['freq'], self.signal['amp'] = list_input[0], list_input[1]
            if self.signal['wave_type'] in ['SINE', 'SQUARE']:
                self.signal['duty'] = list_input[2]
        except:
            self.plot_entry_freq.insert(0, "Invalid input: ")
        self.figure.suptitle(self.signal['wave_type'])
        self.plot_signal()
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
