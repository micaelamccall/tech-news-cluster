import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.utils import validation
from sklearn.externals import joblib



# Load cleaned data
news_df = pd.read_csv('data/clean_content.txt')


# Bag-of-words representation: how many times does each word appear in a document. CountVectorizer creates a bag-of-words by createing a matrix where each feature is a word in the vocabulary and each row is the frequency in each document
# Instead of doing a pure count, you can also scale the feature based on the it's relative frequency. If a word appears a lot in some documents but not in most, it is likely to be informative; if it appears often in most documents, it likely isn't.
# Can do this by vectorizing vocabulary with tf-idf vectorizer (term-frequency inverse-document-frequency)
# Also applies L2 regularization, which makes it so that the length of the document does not change the representation

# Cut back on tokens by using only those that appear in more than 5 documents
# For unsupervized learning, sklearn recommends taking out common words, so I took out words that appear in more than a 15% of documents

vectorizer = TfidfVectorizer(analyzer = 'word', min_df = 5, ngram_range = (1,3), max_df = 0.15)

# Returns the sparse tf-idf weighted document-term matrix
X = vectorizer.fit_transform(news_df['clean_content'])

# Save model

if __name__ == '__main__':
    validation.check_is_fitted(vectorizer, '_tfidf')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.sav')

    X.shape

# tf-idf is an unsupervised technique that is meant to determine which words distinguished documents 
# to get that matrix, it multiples the idf (inverse document frequency) vector, which gives scores that appear more frequently accorss documents lower scores because they are deemed to be less important, 
# by the document term frequency

# We can inspect which words tf-idf found most important 
terms = vectorizer.get_feature_names() # get the list of terms in the vocabulary
tfidf = X.todense() # Make the matrix dense 
tfidf_max = np.array(tfidf.max(axis = 0)).ravel() # get the max tfidf weight of each term and flatten to a 1D array

# Plot a word cloud for more frequent and least frequent words
def plot_tfidf_word_cloud(frequencies = tfidf_max, terms = terms, most_frequent = True):

    '''
    Plots a word cloud for the most important or least frequent words in a list
    
    Arguments: 
    frequencies: a (terms,) sized array of frequencies
    terms: a list or array of terms
    most_frequent: if True, plots most frequent, if False, plots least frequent 
    
    Ouput: a word cloud
    
    '''
    # Sort frequency array in ascending and returns an array of indices
    sorted_frequencies = frequencies.argsort()

    # Create word cloud with highest or lowest 75 terms, joined into a string
    if most_frequent == True:
        cloud = WordCloud().generate(text=(' '.join(np.array(terms)[sorted_frequencies[-75:]])))
        title = "Features with highest tf-idf"
    else:
        cloud = WordCloud().generate(text = (' '.join(np.array(terms)[sorted_frequencies[75:]])))
        title = "Features with lowest tf-idf"
    
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    plot_tfidf_word_cloud()
    plot_tfidf_word_cloud(most_frequent = False)
# Lower scores mean less informative, higher mean more
