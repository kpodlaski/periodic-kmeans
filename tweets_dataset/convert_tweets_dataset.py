import json
from enum import Enum
import numpy as np

import pandas as pd

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans
import matplotlib.pyplot as plt

from periodic_kmeans.periodic_kmeans import PeriodicKMeans


def tweets_from_json_to_csv():
    chunksize = 10 ** 6
    for chunk in pd.read_json("../_data/in/tweets/tweets-nov-2012.json",
            lines=True, orient='records', chunksize=chunksize):
        chunk = chunk.drop(['hashtags', 'user_id', 'urls'], axis=1)
        chunk['hour']=chunk['timestamp'].dt.hour
        chunk['minute'] = chunk['timestamp'].dt.minute
        chunk['second'] = chunk['timestamp'].dt.second
        chunk['dweek'] = chunk['timestamp'].dt.weekday
        chunk.to_csv("../_data/in/tweets/tweets.csv", sep=';', mode='a', header=False)

def tweets_time_to_float():
    chunksize = 10**6
    for chunk in pd.read_json("../_data/in/tweets/tweets-nov-2012.json",
                              lines=True, orient='records', chunksize=chunksize):
        chunk = chunk.drop(['hashtags', 'user_id', 'urls'], axis=1)
        chunk['time'] = chunk['timestamp'].dt.hour + (chunk['timestamp'].dt.minute/60)+(
            (chunk['timestamp'].dt.second)/3600)
        chunk['dweek'] = chunk['timestamp'].dt.weekday
        chunk['weektime'] = chunk['dweek']+chunk['time']/24
        chunk.to_csv("../_data/in/tweets/tweets_3.csv", sep=';', mode='a', header=False)

class TweetsDataTypes(Enum):
    RAW = 0
    DAYLY = 1
    WEEKLY = 2

def read_dataset(type, sample = None):
    data = pd.read_csv("../_data/in/tweets/tweets_3.csv", sep=';')
    if sample is not None:
        if sample > 1 :
            data = data.sample(n=sample)
        if sample < 1 :
            data = data.sample(frac=sample)
    if type == TweetsDataTypes.RAW:
        return data.values
    if type == TweetsDataTypes.DAYLY:
        return data[['time']].values
    if type == TweetsDataTypes.WEEKLY:
        return data[['weektime']].values

def draw_histogram(data, bins, clusters = None, kmeans=None, periodic = False, save_to_file=None):
    fig = plt.figure()
    if clusters == None:
        clusters = [1]
        _cluster_data = data
    for cl in clusters:
        if kmeans is not None:
            if periodic:
                _cluster_data = km.periodic_shift(data[cl])
            else:
                _cluster_data = data[cl]
        plt.hist(_cluster_data, bins=bins)
    if save_to_file is not None:
        plt.savefig("../_data/out/"+save_to_file)
    plt.show()

params_settings ={ TweetsDataTypes.WEEKLY :{
                                            'period': 7,
                                            'no_of_clusers': 7,
                                            'file_postfix': 'week',
                                           },
                    TweetsDataTypes.DAYLY :{
                                            'period': 24,
                                            'no_of_clusers': 2,
                                            'file_postfix': 'day',
                                           },
        }


def periodic_shift_by_angle(points, period, shift):
    _points = np.array([x+period if x < shift else x for x in points]).reshape(-1, 1)
    return _points

#tweets_from_json_to_csv()
#tweets_time_to_float()

data_type = TweetsDataTypes.WEEKLY

params = params_settings[data_type]

####DO THE JOB
bins_per_cluster = 20
no_of_clusters = params['no_of_clusers']
##Initial data
times = read_dataset(data_type)

#times = np.random.choice(times.reshape(-1),int(len(times)/12)).reshape(-1,1)
# print(times, max(times), min(times), times.shape)

draw_histogram(times, bins_per_cluster*no_of_clusters, save_to_file="hist_a_{0}.png".format(params['file_postfix']))

#print(times)
##Classical

no_of_clusters = 7
initial_centers = kmeans_plusplus_initializer(times, no_of_clusters).initialize()
km = kmeans(times, initial_centers)
##Periodic
##km = PeriodicKMeans(times, period=params['period'], no_of_clusters=no_of_clusters)

km.process()
clusters = km.get_clusters()
centers = km.get_centers()
wccs = km.get_total_wce()
print(wccs)
print("centers:", centers)

result = {"clusters": clusters, "centers": centers, "wccs": wccs}
with open('../_data/out/tweets/clust_periodic_{0}.json'.format(params['file_postfix']), 'w') as outfile:
    json.dump(result, outfile)
fig = plt.figure()

draw_histogram(times, bins_per_cluster, clusters=clusters, kmeans=km, periodic=False, save_to_file="hist_b_{0}.png".format(params['file_postfix']))

