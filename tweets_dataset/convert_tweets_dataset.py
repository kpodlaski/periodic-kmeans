import json

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


#tweets_from_json_to_csv()
#tweets_time_to_float()

bins_per_cluster = 20
no_of_clusters = 7

data = pd.read_csv("../_data/in/tweets/tweets_3.csv", sep=';')
#times = data[['time']].values
times = data[['weektime']].values

fig = plt.figure()
plt.hist(times, bins=bins_per_cluster*no_of_clusters)
plt.show()
plt.savefig("../_data/out/hist_a.png", format="png")

#print(times)
##Classical
##initial_centers = kmeans_plusplus_initializer(times, no_of_clusters).initialize()
##km = kmeans(times, initial_centers)
##Periodic
km = PeriodicKMeans(times, period=7, no_of_clusters=no_of_clusters)



km.process()
clusters = km.get_clusters()
centers = km.get_centers()
print("classical:",centers)
print("centers:",centers)

result = {"clusters":clusters, "centers":centers}
with open('../_data/out/tweets/clust_periodic_7.json', 'w') as outfile:
    json.dump(result, outfile)
fig = plt.figure()


fig = plt.figure()
for cl in clusters:
    _cluster_data = km.periodic_shift(times[cl])
    plt.hist(_cluster_data, bins=bins_per_cluster)
plt.show()
plt.savefig("../_data/out/hist_b.png", format="png")