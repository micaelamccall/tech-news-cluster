from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

# Load cleaned data
news_df = pd.read_csv('data/clean_content.txt')

# Load vectorizer 
vectorizer = joblib.load('models/tfidf_vectorizer.sav')

X = vectorizer.transform(news_df['clean_content'])

# SVD is a dimensionality reduction technique, which is often used for latent semantic analysis and works on tf-idf matrices. 
# This way, latent patterns in the term frequencies can be identified, 
# which may convey more semantic information that is then used in the KMeans clustering.


svd = TruncatedSVD(n_components=100, random_state=42)
normalizer = Normalizer(copy=False)

svd_pipe = make_pipeline(svd, normalizer)

# According to the SKlearn documentation, vectorizer results are normalized, which makes KMeans behave as
# spherical k-means for better results. Since LSA/SVD results are
# not normalized, we have to redo the normalization.

X_svd = svd_pipe.fit_transform(X)

X_svd.shape

# Choose the best number of k for this new dataset and train the model
from kmeans import choose_k, plot_silhouette_scores
choose_k(25, X_svd)

k = 10

kmeans_svd =  KMeans(n_clusters = k, init = 'k-means++', random_state= 42)

cluster_labels_svd = kmeans.fit_predict(X_svd)

joblib.dump(kmeans, 'models/kmeans_svd.sav')

plot_silhouette_scores(X_svd, k)


# Print words with top tfidf scores in each cluster
# Can't print top words according to cluster centers because the centers correspond to components of the features not the actual terms
from feature_extraction import tfidf, terms

def print_max_tfidf_per_term_per_cluster(cluster_labels):
    tfidf_df = pd.DataFrame(tfidf, columns = terms)
    tfidf_df['cluster_label'] = cluster_labels

    max_tfidf_per_term_per_cluster={}
    for label in tfidf_df.cluster_label:
        max_tfidf_per_term_per_cluster[label]=(np.array(tfidf_df[tfidf_df.cluster_label == label].max(axis = 0)).ravel())
    max_tfidf_per_term_per_cluster = pd.DataFrame(max_tfidf_per_term_per_cluster)

    for i in range(k):

        sorted_tfidf = np.array(max_tfidf_per_term_per_cluster[i].argsort())[::-1][:][:15]
        print("Cluster %d:" % i, end='')
        for ind in sorted_tfidf[:15]:
            if terms[ind-1].find(' ') == -1:
                print(' %s' % terms[ind], end='')
        print()


print_max_tfidf_per_term_per_cluster(cluster_labels_svd)