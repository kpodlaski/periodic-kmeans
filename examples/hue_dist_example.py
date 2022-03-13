import glob
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import distance_metric, type_metric

from measures.measures import roller2D
from periodic_kmeans.energy_periodic_kmeans import periodic_kmeans2D

roller_distance = lambda a,b : roller2D(a,b)

data = pd.DataFrame()
for file in glob.glob("../_data/in/hue/Residential_*.csv"):
    rdata = pd.read_csv(file,sep=",");
    rdata['date']=pd.to_datetime(rdata['date'])
    fname = os.path.basename(file)
    rdata.loc[:,'residence'] = fname
    data = pd.concat([data,rdata])
mask = (data['date'] >= '2019-01-01') & (data['date'] < '2019-03-01')
sel_data= data.loc[mask]
#sel_data = data
sel_data = sel_data.groupby('hour').median()
print(sel_data)
x = range(len(sel_data))
fig = plt.figure()
plt.title("classical")
#plt.scatter(sel_data['hour'],sel_data['energy_kWh'])
plt.scatter(x,sel_data['energy_kWh'])
plt.show()
print(max(data['energy_kWh']))
sel_data['h']=(np.array(list(range(0,24)))+6)%24
kWhData= sel_data[['h','energy_kWh']].values
print(kWhData)
initial_centers = kmeans_plusplus_initializer(kWhData, 3).initialize()
km = kmeans(kWhData, initial_centers)
km.process()
clusters = km.get_clusters()
print("classical:",clusters)
fig = plt.figure()
for cl in range(len(clusters)):
    points = kWhData[clusters[cl]]
    plt.scatter( points[:,0],points[:,1])
plt.show()

metric = distance_metric(type_metric.USER_DEFINED, func=roller_distance)
km_periodic = periodic_kmeans2D(kWhData,initial_centers, metric = metric)
km_periodic.process()
clusters = km.get_clusters()
print("periodic",clusters)
fig = plt.figure()
plt.title("priodic")
for cl in range(len(clusters)):
    points = kWhData[clusters[cl]]
    plt.scatter( points[:,0],points[:,1])
plt.show()
