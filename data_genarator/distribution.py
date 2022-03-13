import math


class Distribution():
    def d(x):
        return None

class Gauss_distribution(Distribution):
    def __init__(self, factor, mean, sigma):
        self.mean = mean
        self.sigma=sigma
        self.factor=factor

    def d(self,x):
        f = self.factor * math.exp(-((x - self.mean) / self.sigma) ** 2)
        return f

class Multi_Gauss_distribution(Distribution):
    def __init__(self, factors, means, sigmas):
        self.distributions = list()
        for i in range(min(len(factors), len(means), len(sigmas))):
            dist = Gauss_distribution(factors[i],means[i],sigmas[i])
            self.distributions.append(dist)

    def d(self,x):
        f = 0;
        for i in range(len(self.distributions)):
            f += self.distributions[i].d(x) / (i + 1)
        return f


class Flat_distribution(Distribution):

    def __init__(self,factor):
        self.value = factor

    def d(self,x):
        return self.value

class Exp_distribution(Distribution):

    def __init__(self, factor, alpha):
        self.factor = factor
        self.alpha=alpha

    def d(self,x):
        return self.factor*math.exp(self.alpha*x)


class Log_distribution(Distribution):

    def __init__(self, factor, alpha, base=2):
        self.factor = factor
        self.alpha = alpha
        self.base = base

    def d(self, x):
        return self.factor * math.log(self.alpha * x,self.base)

class Triangle_distribution(Distribution):

    def __init__(self, x1, y1,x2, y2):
        self.a = (self.y2 - self.y1) / (self.x1 - self.x2)
        self.x0 = min(x1,x2)
        if self.x0==x1:
            self.y0 = y1
        else:
            self.y0 = y2


    def __init__(self,a, x0, y0):
        self.a = a
        self.x0 = x0
        self.y0=y0

    def d(self, x):
        return self.a *(x-self.x0) + self.y0