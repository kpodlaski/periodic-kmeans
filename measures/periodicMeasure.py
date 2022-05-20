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
        # metric should be distance ^2
        d = math.sqrt((a - b) * (a - b))
        return (min(d, self.period - d))**2

    def periodic_mean(self,points):
        _n = len(points)
        mask = np.array([0 if x > self.period / 2 else 1 for x in points]).reshape(-1, 1)
        _l_n = mask.sum()
        _l_r = _n - _l_n
        if _l_n > 0 and _l_n < _n:
            _mean_left = (points*mask).sum(axis=0)/_l_n
            _mean_right = (points*(1-mask)).sum(axis=0)/(_l_r)
            return self.perodic_two_points_mean(_mean_left, _mean_right, _l_n, _l_r )
        else :
            return points.mean(axis=0)

    def perodic_two_points_mean(self, pointL, pointR, wL=1, wR =1):
        if pointR<pointL :
            return self.perodic_two_points_mean(pointR,pointL,wR, wL)
        _mean = (wL*pointL+wR*pointR)/(wL+wR)
        if abs(pointL-pointR)> self.period/2:
            _mean += wL*self.period/(wL+wR)
            _mean = _mean % self.period
        return _mean
