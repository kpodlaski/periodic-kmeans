def euclidean1D(valA, valB):
    return abs(valA-valB)

# minimal angle between alpha and beta
def angle1D(alpha, beta):
    d = abs(alpha - beta)
    return min(d, 360-d)

def hour1D(h1, h2):
    d = abs(h1 - h2)
    return min(d, 24-d)

def week1D(h1, h2):
    d = abs(h1 - h2)
    return min(d, 7-d)

def unitperiod1D(h1,h2):
    d= abs(h1-h2)
    return min(d,1-d)


def roller2D(a, b):
    d = euclidean1D(a[1],b[1])**2
    d+= (hour1D(a[0],b[0]))**2
    return d