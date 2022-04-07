import types

import numpy  as np
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import distance_metric, type_metric

from measures.periodicMeasure import PeriodicMeasure


def periodic_mean(points):
    if max(points) - min(points)> 300:
        _points = np.array([0 if x > 180 else 360 for x in points]).reshape(-1,1)
        _points = points + _points
        return _points.mean(axis=0)
    else:
        return points.mean(axis=0)

def _periodic_update_centers(self):
    dimension = self._kmeans__pointer_data.shape[1]
    centers = np.zeros((len(self._kmeans__clusters), dimension))

    for index in range(len(self._kmeans__clusters)):
        cluster_points = self._kmeans__pointer_data[self._kmeans__clusters[index], :]
        centers[index] = periodic_mean(cluster_points)
    return np.array(centers)

def periodic_kmeans(data, initial_centers, metric):
    kmeans_instance =  kmeans(data, initial_centers, metric=metric)
    kmeans_instance._kmeans__update_centers = types.MethodType(_periodic_update_centers,kmeans_instance)
    return kmeans_instance


class PeriodicKMeans(kmeans):

    def __init__(self, data, period, initial_centers = None, no_of_clusters = None):
        self.data = data
        self.period = period
        self.measure = PeriodicMeasure(period)
        self.metric = distance_metric(type_metric.USER_DEFINED, func=self.measure.distance)
        _centers = initial_centers
        if _centers == None:
            _centers = initial_centers = kmeans_plusplus_initializer(data, no_of_clusters).initialize()
        print(_centers)
        super().__init__(data, _centers, metric=self.metric)
        self._kmeans__update_centers = types.MethodType(_periodic_update_centers, self)

    def clustering(self):
        self.process()
        clusters = self.get_clusters()
        clust_data = []
        for c in range(len(clusters)):
            clust_data.append(np.array(self.data[clusters[c]]))
        return clust_data, self.get_total_wce(), self.get_centers()

    def periodic_shift(self, data):
        return self.measure.periodic_shift(data)





