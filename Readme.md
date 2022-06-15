
# Introduction

The repository is devoted to the modification of the k-means algorithm that takes into account periodic boundary conditions. The details of the approach are published in the article: Miniak-Górecka, A.; Podlaski, K.; Gwizdałła, T. Using K-Means Clustering in Python with Periodic Boundary Conditions. Symmetry 2022, 14, 1237. https://doi.org/10.3390/sym14061237
 
The implementation uses pyclustering library as a base. The main modification is enclosed in PeriodicKmeans class.

The three exemplary usages of the approach is in the [package examples](examples).

# Usage
The implementation requires library [pyclustering] (https://pyclustering.github.io/). 

Thus it has to be installed for example, using pip:
```
    $pip install pyclustering
```

The implementation require two packages from the repository [measures](measures) and [periodic_kmeans](periodic_kmeans). The first introduces class [PeriocicMeasure](measures/periodicMeasure.py). The second introduce class [PeriodicKMeans](periodic_kmeans/periodic_kmeans.py).
The usage of the implementation is shown for three different datasets in [examples](examples)

Initialization of k-means object, with given:
 - data - data to be clusterized
 - period - that is specific to the dataset 
 - no_of_clusters - number of clusters we want to obtain
 
```
kmeans2 = PeriodicKMeans(data, period=360, no_of_clusters=n_clusters)
``` 
The clusterization is straightforward:
```
clust_data, wccs_circ, centers = kmeans2.clustering()
```
the method clustering returns:
- clust_data - data points are divided into clusters
- wccs_circ - the value of wccs (within-cluster sum of a squares) using a periodic distance measure
- centers - list of centers found by the method.

# Examples
The package [examples](examples) contains three different usages of the approach. 
- [modal data](examples/modal_dist_example.py) - artificial dataset built as interference of three gaussian modes. The period for this data is equal to 1.0
- [wind direction](examples/wind_dir_example.py) - real dataset containing results of wind direction measurements. The period for this data is equal to 360.0
- [nyc taxi](examples/nyc_taxi_example.py) - dataset of pickup date from [NYC Taxi dataset](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml). For this data, we use two seasonal periods a day and a week. It is possible to try the period set to month or year.



# License
The code is free to use under MIT type license. Licence details are in file [license.txt](license.txt). 

If you find this work useful in your research, please cite:

    @article{periodic-kmeans2022,  
    author = {Alicja, Miniak-G{\'{o}}recka and Krzysztof, Podlaski and Tomasz Gwizda{\l}{\l}a},
    title = {Using k-means clustering in python with periodic boundary conditions},
    journal = {Symmetry},
    volume = {14},
    number = {6},
    article-number= {1237},
    year = {2022},
    doi = {10.3390/sym14061237},
    year = {2022},
    }
    
  
