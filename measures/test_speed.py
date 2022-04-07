import timeit
import numpy as np

from periodicMeasure import PeriodicMeasure

a = np.random.rand(10000).reshape(-1,1)
pmeasure = PeriodicMeasure(1)

def test():
    pmeasure.periodic_shift2(a)

def test2():
    pmeasure.periodic_shift(a)

def mean1():
    return pmeasure.periodic_mean_old(a)

def mean2():
    return pmeasure.periodic_mean(a)


print("test()")
print(timeit.timeit('test()', setup="from __main__ import test", number=100) )

print("test2()")
print(timeit.timeit('test2()', setup="from __main__ import test2", number=100) )

print("mean2()", mean2())
print(timeit.timeit('mean2()', setup="from __main__ import mean2", number=100) )

print("mean1()", mean1())
print(timeit.timeit('mean1()', setup="from __main__ import mean1", number=100) )

