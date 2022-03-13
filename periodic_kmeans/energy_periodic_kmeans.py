import types

import numpy as np
from pyclustering.cluster.kmeans import kmeans

def periodic_mean2D(points):
    if max(points[:,0]) - min(points[:,0])> 15:
        _temp = points[:,0]
        _points = np.array([0 if x > 12 else 24 for x in _temp]).reshape(-1,1)
        _points = _temp + _points
        return np.array([_points.mean(), points[:,1].mean(axis=0)])
    else:
        return points.mean(axis=0)

def _periodic_update_centers2D(self):
    dimension = self._kmeans__pointer_data.shape[1]
    centers = np.zeros((len(self._kmeans__clusters), dimension))

    for index in range(len(self._kmeans__clusters)):
        cluster_points = self._kmeans__pointer_data[self._kmeans__clusters[index], :]
        centers[index] = periodic_mean2D(cluster_points)
    return np.array(centers)

def periodic_kmeans2D(data, initial_centers, metric):
    kmeans_instance =  kmeans(data, initial_centers, metric=metric)
    kmeans_instance._kmeans__update_centers = types.MethodType(_periodic_update_centers2D,kmeans_instance)
    return kmeans_instance




