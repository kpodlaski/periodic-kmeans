import bisect
import datetime
from enum import Enum
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyclustering.cluster.kmeans import kmeans
from periodic_kmeans.periodic_kmeans import PeriodicKMeans


class GeoDataQuality(Enum):
    HQ = 0
    MQ = 1
    LQ = 2


def _read_fco(file_name, shuffle=False, data_quality=GeoDataQuality.LQ):
    df = pd.read_csv(file_name, sep=';')
    if shuffle :
        df = df.sample(frac=1)
    df = df[df['fco2_raw'].notna()]
    if data_quality == GeoDataQuality.HQ:
        df = df[df['fco2_HQ'].notna()]
    if data_quality == GeoDataQuality.MQ:
        df = df[df['fco2_MQ'].notna()]
    df = df.drop(['class'], axis=1)
    return df

base_path = "../_data/in/geo/"
outdir = "../_data/out/geo/"

def read_fco_all(filename = base_path+'d_fco2_all.csv',shuffle=False, division=None):
    return _read_fco(filename,shuffle=shuffle, data_quality = GeoDataQuality.LQ)

def read_fco_mq(filename = base_path+'d_fco2_all.csv', shuffle=False, division=None):
    return _read_fco(filename,shuffle=shuffle, data_quality = GeoDataQuality.MQ)

def read_fco2_hq(filename= base_path+'d_fco2_hq.csv', shuffle=False, division=None):
    return _read_fco(filename, shuffle=shuffle, data_quality = GeoDataQuality.HQ)

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
        raise (Exception("Huston we have a problem"))
    kmeans_instance.process()


    clusters = kmeans_instance.get_clusters()
    clust_data = []
    for c in range(len(clusters)):
        clust_data.append(np.array(data[clusters[c]]))
        #print("cluster", c, min(clust_data[c]), max(clust_data[c]))
    print(kmeans_instance.get_centers())
    print(kmeans_instance.get_total_wce())
    return clust_data, kmeans_instance.get_total_wce(), kmeans_instance.get_centers()



data_df = read_fco2_hq()

data_df['yday'] = data_df.apply(lambda x: datetime.datetime(int(x['rok']),int(x['ms']),int(x['dz'])).timetuple().tm_yday, axis=1)

fout = open(outdir+"geo_results.tex", "w")

xlabels = {'yday':'day of the year',
           'godz':'time of a day'}

params = [
    {'dataset':'yday', 'period':365, 'scale':False, 'n_clusters':[4]},
    {'dataset':'godz', 'period':24, 'scale':False, 'n_clusters':[4]},
]


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
        fig, ax = plt.subplots(2, figsize=(6.4,6.4))
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
        plt.savefig(outdir+"taxi_{1}_{0}.png".format(n_clusters,data_set), format="png")
        plt.show()

        fout.write("%dataset-{0},\nperiodic&{1}&{2}\n".format(data_set,n_clusters,wccs_circ))
        fout.write("%dataset-{0},\noriginal&{1}&{2}\n".format(data_set,n_clusters,wccs_euc))
        fout.write("%dataset-{0}, n_clusters-{1}, wccs_ratio:{2}\n".format(data_set, n_clusters, wccs_circ/wccs_euc))
        fout.flush()
fout.close()
