# Using k means because you can use the predict method on the new data!!!

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_samples
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from functools import lru_cache

from feature_extraction import news_df

k = 14

pipe = Pipeline([
    ("vectorizer", TfidfVectorizer(analyzer = 'word', min_df = 5, ngram_range = (1,3), max_df = 0.15)),
    ("kmeans", KMeans(n_clusters = k, init = 'k-means++', random_state= 42))
])

kmeans =  KMeans(n_clusters = k, init = 'k-means++', random_state= 42)

cluster_labels = pipe.fit_predict(news_df)


def print_top_words_by_cluster():

    '''
    A function to plot the top terms in each cluster of the kmeans model
    '''
    # The high dimensional coordinates of the center of each cluster (shape is 15 by the number of features)
    # Within each cluster (row) sort the coordinate of each features them in descending order and return array of indices
    sorted_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    # for each of the 15 clusters (15 rows in sorted centroids dataset), print the first several 1 gram words (words with highest coordinate values and thus more important for the cluster)
    for i in range(15):
        print("Cluster %d:" % i, end='')
        for ind in sorted_centroids[i, :15]:
            if terms[ind].find(' ') == -1:
                print(' %s' % terms[ind], end='')
        print()
    
def plot_silhouette_scores():
    '''
    A function to plot the silhouette scores in each cluster of the kmeans model
    '''

    # An array of the silhouette score of each sample (article) 
    sample_sil_values = silhouette_samples(X, cluster_labels)

    fig, (ax1) = plt.subplots(figsize = [10,6])

    # For each cluster, plot the silhouette scores for each sample
    y_lower = 10
    for i in range(15):

        # Values for each cluster
        ith_cluster_sil_values = sample_sil_values[cluster_labels == i]

        ith_cluster_sil_values.sort()

        # How many samples are in that cluster
        size_cluster_i = ith_cluster_sil_values.shape[0]

        # The upper limit of that cluster group is the lower limit plus the size of the cluster
        y_upper = y_lower + size_cluster_i
        
        color = cm.nipy_spectral(float(i) / 15)

        # Fill the length of the silhouette score on the x axis, on the y axis between the upper and lower limits of the cluster group 
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_sil_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.08, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_yticks([])
    ax1.set_xlim([-0.1, 0.4])
    ax1.grid(False)
    ax1.set_ylabel("Cluster Label")
    ax1.set_xlabel("Silhouette scores")
    ax1.set_title("Silhouette Plot for Various Clusters")

