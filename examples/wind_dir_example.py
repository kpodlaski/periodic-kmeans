import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import type_metric, distance_metric

from measures.measures import euclidean1D, angle1D
from periodic_kmeans.periodic_kmeans import periodic_kmeans, PeriodicKMeans

squared_distance = lambda a,b : euclidean1D(a,b) **2
angle_squared_distance = lambda a, b: angle1D(a,b) **2


def k_means_clustering(data, n_clusters, metric=None):
    init_width = 360/n_clusters
    center = init_width/2
    start_centers = []
    while center<360:
        start_centers.append([center])
        center+=init_width
    if metric == None:
        kmeans_instance = kmeans(data, start_centers)
    else:
        kmeans_instance = periodic_kmeans(data, start_centers, metric=metric)
    kmeans_instance.process()


    clusters = kmeans_instance.get_clusters()
    clust_data = []
    for c in range(len(clusters)):
        clust_data.append(np.array(data[clusters[c]]))
        #print("cluster", c, min(clust_data[c]), max(clust_data[c]))
    print(kmeans_instance.get_centers())
    print(kmeans_instance.get_total_wce())
    return clust_data, kmeans_instance.get_total_wce(), kmeans_instance.get_centers()

def shift_dataset(dataset, shift):
    new_data_set = [ x if x>shift else 360+x for x in dataset.reshape(-1)]
    return np.array(new_data_set).reshape(-1, 1)


data_set = 'wdir'

data_df = pd.read_csv("../_data/in/{0}.csv".format(data_set));
data = np.array(data_df[data_set])
data = data.reshape(-1, 1)

fig = plt.plot()
bins = np.linspace(0, 360, 36)
plt.hist(data_df,bins, alpha=0.5, edgecolor='black')
plt.xlabel("angle [deg.]")
plt.ylabel("count")
#plt.title("Wind directory, classical and circular kmeans, k={0}".format(n_clusters))
plt.savefig("../_data/out/wdir_dist.png", format="png")
plt.show()


colors = ['blue','red','violet','yellow','green','orange']
fig, ax = plt.subplots(2)
n_clusters = 2
bins = np.linspace(0, 360, 36)
#CIRCULAR Clustering
print("Circular clustering")
###Non objective way
##metric = distance_metric(type_metric.USER_DEFINED, func=angle_squared_distance)
##clust_data, wccs_circ, centers = k_means_clustering(data, n_clusters, metric)
###Objective way
kmeans2 = PeriodicKMeans(data, period=360, no_of_clusters=n_clusters)
clust_data, wccs_circ, centers = kmeans2.clustering()

clust_order= [1, 0, 2]

print("other:",kmeans2.get_centers())
for c in range(len(clust_data)):
    subset = clust_data[clust_order[c]]
    ax[1].hist(subset, bins=bins, alpha=0.5, label=f"Cluster {c}", edgecolor='black')
for c in centers:
    ax[1].annotate('', xy= (c[0], 0), xytext=(c[0], -1), arrowprops=dict(color='black',  arrowstyle="-|>"))
ax[1].set_title("Periodic k-means")

wccs = 0
for c in range(len(clust_data)):
    for i in range(len(clust_data[c])):
        wccs+= kmeans2.metric(centers[c],clust_data[c][i])
print(wccs)


#Euclidean Clustering
print("Euclidean clustering")
#metric = distance_metric(type_metric.USER_DEFINED, func=squared_distance)
clust_data, wccs_euc, centers = k_means_clustering(data, n_clusters)
for c in range(len(clust_data)):
    subset = clust_data[c]
    ax[0].hist(subset, bins=bins, alpha=0.5, label=f"Cluster {c}", edgecolor='black')
for c in centers:
    ax[0].annotate('', xy= (c[0], 0), xytext=(c[0], -1), arrowprops=dict(color='black',  arrowstyle="-|>"))
ax[0].set_title("Original k-means")

for ticklabel in ax[0].xaxis.get_ticklabels():
    ticklabel.set_visible(False)
plt.xlabel("angle [deg.]")
ax[0].set_ylabel("count")
ax[1].set_ylabel("count")
#plt.title("Wind directory, classical and circular kmeans, k={0}".format(n_clusters))
plt.savefig("../_data/out/wdir_{0}.png".format(n_clusters), format="png")
plt.show()
print("WCCSratio:",wccs_circ/wccs_euc)

print(clust_data)

#results.to_csv("../_data/out/modal_clustr_results.csv", sep = ";")
#results.to_csv("../_data/out/modal_clustr_results.tex", sep = "&", float_format="%.3f", index=False)



# # Other Eucliedan clustering
# kmeans = KMeans(n_clusters=2)
# kmeans.fit(_data)
# kmeans_centers = np.array(kmeans.cluster_centers_)
# print("Classical clustering")
# print(kmeans_centers)
# print(kmeans.inertia_)
