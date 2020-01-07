# Using k means because you can use the predict method on the new data!!!

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from feature_extraction import X

# Without group truth labels with which to evaluate kmeans, detemining parameters like number of clusters can be difficult
# There are other metrics to evaluate kmeans. One is the within cluster sum of squared errors (distortion). Lower scores mean tighter clusters.
# Silhouette score measures the distance between clusters by measuring how close each point in one cluster is to the neighboring cluster. A measure between [-1,1], higher scores mean more distinct clusters
# The best number of clusters will be when the SSE curve bends, and that maximizes silhouette score

def choose_k(max_k):
    '''
    A function to display plots of average silhouette score and average SSE (inertia) for various numbers of clusters

    Arguments: max_k = the maximum number of clusters to test 

    Ouput: line plots for both silhouette scores and SSE
    '''

    # Initialize empty lists
    distortions = []
    sil_score = []

    # For each value of k, initialize and fit a MiniBatchKMeans and append the sillhouette score and SSE to the lists
    for k in range(2, max_k):
        kmeans = MiniBatchKMeans(n_clusters = k, init = 'k-means++', max_iter = 1000, random_state=42)
        kmeans.fit(X)
        sil_score.append(silhouette_score(X, kmeans.labels_))
        distortions.append(kmeans.inertia_)

    # Plot each score for each number of clusters
    sns.set(style="whitegrid")
    distortions_plot = sns.lineplot(x= range(2,max_k),y= distortions)
    plt.ylabel("Sum of Squared Errors (distortion)")
    plt.xlabel("Number of clusters")
    distortions_plot.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.show()
    plt.close()

    silhouette_plot = sns.lineplot(x= range(2,max_k),y= sil_score)
    plt.ylabel("Silhouette score")
    plt.xlabel("Number of clusters")
    silhouette_plot.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.show()

if __name__ == '__main__':
    choose_k(25)