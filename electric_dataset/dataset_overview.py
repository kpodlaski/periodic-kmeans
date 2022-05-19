import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn import preprocessing


def convertDate(d):
    return dt.datetime.fromisoformat(d)

sample_start = dt.date(2017,1,1)
sample_end = dt.date(2019,1,1)



data_df = pd.read_csv("../_data/in/electricity/be.csv");
print(data_df)
data_df['sdate'] = pd.to_datetime(data_df['start'].apply(convertDate))
data_df['edate'] = pd.to_datetime(data_df['end'].apply(convertDate))
data_df['time'] = data_df['sdate'] + (data_df['edate'] - data_df['sdate'])/2

sample_df = data_df.loc[data_df['time'].dt.date >= sample_start]
sample_df = sample_df.loc[sample_df['time'].dt.date < sample_end]
min = sample_df['load'].min()
max = sample_df['load'].max()
factor = max - min
#sample_df['load']=100*(sample_df['load']-min)/(factor)
sample_df['load']=100*(sample_df['load'])/(max)

x= sample_df['sdate']
print(sample_df['load'].sum())
fig = plt.plot()
plt.scatter(x=x, y=sample_df['load'], s=1)
plt.xlabel("date")
plt.ylabel("energy demand [MWh]")
plt.show()

enumerate = 0
electicity_data = None
for ammount in sample_df['load']:
    sample = np.linspace(enumerate, enumerate+1, int(ammount))
    enumerate+=1
    if electicity_data is None:
        electicity_data = sample
    else:
        electicity_data = np.concatenate((electicity_data,sample))
print(len(electicity_data))

np.savetxt('../_data/in/electricity/sample.csv', electicity_data, delimiter=",")
bins = np.linspace(0, len(electicity_data)+1, 1000)
fig = plt.plot()
plt.hist(electicity_data, bins=bins)
plt.xlabel("date")
plt.ylabel("energy demand [MWh]")
plt.show()


