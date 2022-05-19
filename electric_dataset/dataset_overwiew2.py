import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


electicity_data = np.loadtxt('../_data/in/electricity/sample.csv', delimiter=",")
bins = np.linspace(0, 100, 100)
fig = plt.plot()
plt.hist(electicity_data, bins=100)
#plt.scatter(bins, electicity_data)
plt.xlabel("date")
plt.ylabel("energy demand [MWh]")
plt.show()
