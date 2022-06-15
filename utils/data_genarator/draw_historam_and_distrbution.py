import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_sets= ['3modal', '4modal', 'exp', 'gauss', '3modal_2', '3modal_3', 'tgrunt']


for data_set in data_sets:
    data = pd.read_csv("../../_data/in/{0}.csv".format(data_set));
    tgrunt = np.array(data[data_set])
    plt.hist(tgrunt,50, density=True, histtype="step", cumulative=True, label="CDF")
    plt.title("{0} Cuumullative Distribution Function".format(data_set))
    plt.savefig("../../_data/out/distributions/{0}__CFC.png".format(data_set))
    plt.show()