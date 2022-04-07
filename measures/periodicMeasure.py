import math
import numpy as np

def periodic_point_shift(x, half_period, period):
    if x < half_period:
        return x+period
    return x

class PeriodicMeasure:
    def __init__(self, period):
        self.period = period
        self.half_period = period/2
        #_p_shift = lambda x: periodic_point_shift(x,self.half_period,self.period)
        #self.periodic_shift2 = np.vectorize(_p_shift)

    def distance(self, a, b):
        d = math.sqrt((a-b)*(a-b))
        return min (d, self.period - d)

    def periodic_shift(self,points):
        if max(points) - min(points) > self.period/2:
            _points = np.array([0 if x > self.period/2 else self.period for x in points]).reshape(-1, 1)
            _points = points + _points
            return _points
        else:
            return points

    def periodic_mean(self,points):
        shift = np.count_nonzero(points < self.half_period)
        _mean =  points.mean(axis=0) + shift * self.period / len(points)
        if _mean > self.period:
            return _mean - self.period
        else:
            return _mean


    def periodic_mean_old(self,points):
        _mean = self.periodic_shift(points).mean(axis=0)
        # if max(points) - min(points) > self.period/2:
        #     _points = np.array([0 if x > self.period/2 else self.period for x in points]).reshape(-1, 1)
        #     _points = points + _points
        #     _mean = _points.mean(axis=0)
        # else:
        #     _mean = points.mean(axis=0)
        return _mean
        #if _mean > self.period:
        #    return _mean - self.period
        #else:
        #    return _mean

    def periodic_mean_old(self,points):
        if max(points) - min(points) > self.period/2:
            _points = np.array([0 if x > self.period/2 else self.period for x in points]).reshape(-1, 1)
            _points = points + _points
            _mean = _points.mean(axis=0)
        else:
            _mean = points.mean(axis=0)
        if _mean > self.period:
            return _mean - self.period
        else:
            return _mean