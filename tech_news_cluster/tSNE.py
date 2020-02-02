import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
import pandas as pd

from feature_extraction import tfidf, X_svd
from kmeans import cluster_labels

def tsne_plot(array):
    '''
    A function to plot a tsne plot
    
    Arguments: 
        array: a dense ndarray
        
    Output: prints a plot
    '''
    # t-SNE is a feature reduction technique that reduces features to 2 dimensions, mainly used just for plotting purposes
    tsne=TSNE(random_state = 42)

    # Array with 2 dimensions for each sample
    tsne_features=tsne.fit_transform(array)

    # Data frame of cluster labels and t-SNE features for plotting
    tsne_df = pd.DataFrame({'clusters':cluster_labels, 'tsne0':tsne_features[:,0], 'tsne1':tsne_features[:,1]})
    tsne_df['clusters'] = tsne_df['clusters'].astype('category', ordered = True)

    # Palette for plotting
    palette = ['#7e1e9c', '#ac4f06', '#c87f89', '#e50000',  '#ffd1df',  '#f97306', '#fff39a', '#fac205', '#15b01a', '#a7ffb5','#033500',  '#0343df', '#607c8e',  '#95d0fc', '#653700',]
    sns.set(style="whitegrid")

    # Scatterplot colored by cluster label
    sns.scatterplot(data = tsne_df, x="tsne0", y="tsne1", hue="clusters", palette=palette)
    plt.legend(loc='upper center', bbox_to_anchor=(1.2, 1.1), ncol=1)

    plt.show()


tsne_plot(tfidf)
tsne_plot(X_svd)