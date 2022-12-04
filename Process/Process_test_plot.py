import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#data

from matplotlib import rcParams
rcParams['figure.figsize'] = (15,10)
rcParams['font.size'] = 22


def draw(data, fmt=['r.'], labels=[''], label_x='', label_y='', title=''):
  for array, format, label in zip(data, fmt, labels):
    lists = sorted(array.items()) # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples
    plt.plot(x, y, format, label=label)
  plt.grid(True, which='both')
  # plt.axhline(y=0, color='k')
  # plt.axvline(x=0, color='k')
  # plt.set_aspect('equal')
  
  
x1 = np.array(data[0][2:22].astype('float'))
x1 = x1 / 1575
y1 = np.array(data[1][2:22].astype('float'))
y1 = y1 / np.max(y1)
obj1 = dict(zip(x1, y1))

x2 = np.array(data[2][2:19].astype('float'))
x2 = x2 / 1575
y2 = np.array(data[3][2:19].astype('float'))
y2 = y2 / np.max(y2)
obj2 = dict(zip(x2, y2))
l = min(np.min(x1), np.min(x2))
r = max(np.max(x1), np.max(x2))
draw([obj1, obj2], fmt=['r.', 'b.'], title=r'', labels=['R=Ohm', 'R=100Ohm'])
plt.plot([l, r], [0.707, 0.707], 'g-', label=r'$\frac{1}{\sqrt{2}}$')

plt.title(r'$\frac{U}{U_0} (\frac{\nu}{\nu_0})$')
plt.xlabel(r'$\frac{\nu}{\nu_0}, 1$')
plt.ylabel(r'$\frac{U}{U_0}$, 1')

plt.legend()
plt.show()
