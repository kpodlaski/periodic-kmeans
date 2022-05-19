import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyclustering.cluster.kmeans import kmeans
from measures.measures import euclidean1D, angle1D, week1D, unitperiod1D, hour1D
from periodic_kmeans.periodic_kmeans import periodic_kmeans, PeriodicKMeans

squared_distance = lambda a,b : euclidean1D(a,b) **2
week_squared_distance = lambda a, b: week1D(a,b) **2
unit_period_squared_distance = lambda a, b: unitperiod1D(a,b) **2
hour_squared_distance = lambda a, b: hour1D(a,b) **2

def k_means_clustering(data, n_clusters, period=None, metric=None):
    if period is None:
        period = data.max()
    init_width = period/n_clusters
    center = init_width/2
    start_centers = []
    while center<period:
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

def shift_dataset(dataset, period):
    new_data_set = [ x if x>period/2 else period+x for x in dataset.reshape(-1)]
    return np.array(new_data_set).reshape(-1, 1)

xlabels = {'day_time':'time of the day',
            'month_time':'day of the month',
            'week_time':'day of the week'}

basedir = "../_data/in/nyc_taxi/"
datafile = "test_norm_data.csv"

data_df = pd.read_csv(basedir+datafile)

params = [
    {'dataset':'day_time', 'period':24, 'scale':True, 'n_clusters':[4,5,7,12]},
    {'dataset':'week_time', 'period':7, 'scale':False, 'n_clusters':[3,4,5,7]},
    {'dataset':'month_time', 'period':1, 'scale':False, 'n_clusters':[4,5,7,12]},
]

fout = open("../_data/out/taxi_results.tex", "w")
for par in params:
    for n_clusters in par['n_clusters']:
        data_set = par['dataset']
        period = par['period']
        data = np.array(data_df[data_set])
        data = data.reshape(-1, 1)
        if par['scale']:
            data = data*period

        fig = plt.plot()
        bins = np.linspace(0, period, 70)
        plt.hist(data,bins, alpha=0.5, edgecolor='black')
        plt.xlabel(xlabels[data_set])
        plt.ylabel("count")
        plt.show()

        colors = ['blue','red','violet','yellow','green','orange']
        fig, ax = plt.subplots(2)
        print("Clistering, dataset:{0}, n_clusters:{1}, period:{2}".format(data_set, n_clusters,period))
        #CIRCULAR Clustering
        print("Circular clustering")
        kmeans2 = PeriodicKMeans(data, period=period, no_of_clusters=n_clusters)
        clust_data, wccs_circ, centers = kmeans2.clustering()

        clust_order = list(range(n_clusters))
        # clust_order= [0, 1, 2]
        # if len(clust_order)<n_clusters:
        #     clust_order = list(range(n_clusters))

        fout.write("%periodic&{0}\n".format(kmeans2.get_centers()))
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

        #Euclidean Clustering
        print("Euclidean clustering")
        #metric = distance_metric(type_metric.USER_DEFINED, func=squared_distance)
        clust_data, wccs_euc, centers = k_means_clustering(data, n_clusters)
        fout.write("%original&{0}\n".format(centers))
        for c in range(len(clust_data)):
            subset = clust_data[c]
            ax[0].hist(subset, bins=bins, alpha=0.5, label=f"Cluster {c}", edgecolor='black')
        for c in centers:
            ax[0].annotate('', xy= (c[0], 0), xytext=(c[0], -1), arrowprops=dict(color='black',  arrowstyle="-|>"))
        ax[0].set_title("Original k-means")

        for ticklabel in ax[0].xaxis.get_ticklabels():
            ticklabel.set_visible(False)
        plt.xlabel(xlabels[data_set])
        ax[0].set_ylabel("count")
        ax[1].set_ylabel("count")
        plt.savefig("../_data/out/taxi_{1}_{0}.png".format(n_clusters,data_set), format="png")
        plt.show()

        fout.write("%dataset-{0},\nperiodic&{1}&{2}\n".format(data_set,n_clusters,wccs_circ))
        fout.write("%dataset-{0},\noriginal&{1}&{2}\n".format(data_set,n_clusters,wccs_euc))
        fout.write("%dataset-{0}, n_clusters-{1}, wccs_ratio:{2}\n".format(data_set, n_clusters, wccs_circ/wccs_euc))
        fout.flush()
fout.close()


