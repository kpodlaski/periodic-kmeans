from data_genarator.distribution import Flat_distribution, Exp_distribution, Log_distribution, Triangle_distribution
from data_genarator.multi_modal_gauss import generate_points_from_distribution, save_as_csv, save_as_png, dist_as_png

N= 1000

distributions = {
    'flat' : {
        'dist': Flat_distribution(5),
        'x_min' : 0.1,
        'x_max' : 2,
        'y_max' :5
    },

    'exp-' : {
        'dist' : Exp_distribution(1,-1),
        'x_min' :0.1,
        'x_max' : 4,
        'y_max' : 1
    },
    'exp+' : {
        'dist' : Exp_distribution(1,1),
        'x_min' :0.1,
        'x_max' : 4,
        'y_max' : None
    },
    'log2' : {
        'dist' : Log_distribution(3,1),
        'x_min' : 1.1,
        'x_max' : 15,
        'y_max' : None
    },
    '-log2' : {
        'dist' : Log_distribution(-1,1),
        'x_min' : 0.1,
        'x_max' : 0.9,
        'y_max' : None
    }
    ,
    'triangle' : {
        'dist' : Triangle_distribution(-1/2,0,10),
        'x_min' : 0,
        'x_max' : 20,
        'y_max' : 10
    }
}

distributions['exp+']['y_max'] = distributions['exp+']['dist'].d(distributions['exp+']['x_max'])
distributions['log2']['y_max'] = distributions['log2']['dist'].d(distributions['log2']['x_max'])
distributions['-log2']['y_max'] = distributions['-log2']['dist'].d(distributions['-log2']['x_min'])


for dist_name in distributions.keys():
    dist = distributions[dist_name]['dist']
    y_max = distributions[dist_name]['y_max']
    x_max = distributions[dist_name]['x_max']
    x_min = distributions[dist_name]['x_min']
    points = generate_points_from_distribution(N,dist,x_min, x_max, y_max)
    save_as_csv(points,dist_name)
    save_as_png(points, x_min, x_max, dist_name)
    dist_as_png(dist, x_min, x_max, dist_name)