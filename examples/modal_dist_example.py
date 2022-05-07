import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import type_metric, distance_metric

from cluster_quality.measures import compare_clusters
from measures.measures import euclidean1D, angle1D
from periodic_kmeans.periodic_kmeans import periodic_kmeans

squared_distance = lambda a,b : euclidean1D(a,b) #**2
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
    labels = np.empty(len(data))
    labels.fill(-1)
    for c in range(len(clusters)):
        clust_data.append(np.array(data[clusters[c]]))
        np.put(labels,clusters[c],c)
    #print("centers:", np.array(kmeans_instance.get_centers()).reshape(-1)%360)
    #print("wce:",kmeans_instance.get_total_wce())
    return clust_data, labels, kmeans_instance.get_total_wce(), kmeans_instance.get_centers(), kmeans_instance

def shift_dataset(dataset, shift):
    new_data_set = [ x if x>shift else 360+x for x in dataset.reshape(-1)]
    return np.array(new_data_set).reshape(-1, 1)


data_set = 'modal_gauss'
n_clusters = 4

data_df = pd.read_csv("../_data/in/{0}.csv".format(data_set), sep=";", index_col=0);
clusters = {}
for column in data_df.columns:
    data = np.array(data_df[column])
    data = data.reshape(-1, 1)

    colors = ['blue','red','violet','yellow','green','orange']
    fig, ax = plt.subplots(2)
    #fig.suptitle("Angular modal distribution {1}, classical and circular kmeans, k={0}".format(n_clusters, column))
    bins = np.linspace(0, 360, 100)

    #CIRCULAR Clustering
    #print("Circular clustering")
    metric = distance_metric(type_metric.USER_DEFINED, func=angle_squared_distance)
    clust_data, labels_circ, wccs_circ, centers, k_means = k_means_clustering(data, n_clusters, metric)
    #print(column,k_means.get_clusters())
    centers = np.array(centers)%360

    for c in range(len(clust_data)):
        # for x in clust_data[c]:
        #     #y = [0 for x in clust_data[c]]
        #     y = [0.02,.48]
        #     ax.plot([x,x], y, color=colors[c%len(colors)])
        subset = clust_data[c]
        ax[0].hist(subset, bins=bins, alpha=0.5, label=f"Cluster {c}")
    y = [10 for x in centers]
    #ax[0].scatter(centers, y, s=15)
    for c in centers:
        ax[0].annotate('', xy= (c[0], 0), xytext=(c[0], -1), arrowprops=dict(color='black',  arrowstyle="-|>"))
        #ax[0].annotate('', xy=(c[0], 0), xytext=(c[0], 1), arrowprops=dict(color='red', arrowstyle="-|>"))
    ax[0].set_title("Periodic k-means")
    for ticklabel in ax[0].xaxis.get_ticklabels():
        ticklabel.set_visible(False)


    wccs = 0
    for c in range(len(clust_data)):
        for i in range(len(clust_data[c])):
            wccs+= metric(centers[c],clust_data[c][i])
    #print(wccs)

    #Euclidean Clustering
    #print("Euclidean clustering")
    clust_data, labels_basic, wccs_euc, centers, k_means = k_means_clustering(data, n_clusters)
    #print("circ", k_means.get_clusters())
    for c in range(len(clust_data)):
        # for x in clust_data[c]:
        #     #y = [0 for x in clust_data[c]]
        #     y = [0.52,.98]
        #     ax.plot([x,x], y, color=colors[c%len(colors)])
        subset = clust_data[c]
        ax[1].hist(subset, bins=bins, alpha=0.5, label=f"Cluster {c}")
        y = [10 for x in centers]
    #ax[1].scatter(centers, y, s=15)
    for c in centers:
        ax[1].annotate('', xy= (c[0], 0), xytext=(c[0], -1), arrowprops=dict(color='black',  arrowstyle="-|>"))
        #ax[1].annotate('', xy=(c[0], 0), xytext=(c[0], 1), arrowprops=dict(color='red', arrowstyle="-|>"))
    #ax.legend()
    # fig.suptitle("Angular modal distribution {1}, classical and circular kmeans, k={0}".format(n_clusters, column))
    ax[1].set_title("Original k-means")
    plt.savefig("../_data/out/modal_clustr_ang-{0}.png".format(column), format="png")
    plt.show()


    print("WCCSratio:",wccs_circ/wccs_euc, " for angle ",column)
    clusters[column] = {'basic':labels_basic, 'circ':labels_circ, 'wccs_euc':wccs_euc, 'wccs_circ':wccs_circ, 'wccs_ratio':wccs_circ/wccs_euc}
    #print(column)
    #print(compare_clusters(labels_basic,labels_circ))

results = pd.DataFrame()
for id_col in range(len(data_df.columns)):
    column = data_df.columns[id_col]
    _res = {'angle1': column, 'angle2': column,  'type1': 'basic',  'type2': 'circ'} #, 'wccs_ratio':clusters[column]['wccs_ratio']}
    _res.update(compare_clusters(clusters[column]['basic'], clusters[column]['circ']))
    _pd = pd.DataFrame([_res])
    results = pd.concat([results, _pd], ignore_index=True)
    for type in ['basic', 'circ']:
        for id_col2 in range(id_col+1, len(data_df.columns)):
            column2 = data_df.columns[id_col2]
            for type2 in ['basic', 'circ']:
                _res = {'angle1': column, 'angle2': column2, 'type1': type, 'type2': type2}
                _res.update(compare_clusters(clusters[column][type], clusters[column2][type2]))
                _pd = pd.DataFrame([_res])
                results = pd.concat([results, _pd], ignore_index=True)
#print(results)
results.to_csv("../_data/out/modal_clustr_results.csv", sep = ";")
results.to_csv("../_data/out/modal_clustr_results.tex", sep = "&", float_format="%.3f", index=False)




