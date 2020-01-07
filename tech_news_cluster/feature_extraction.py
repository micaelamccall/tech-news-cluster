# [x] stopwords
# [x] proper nouns
    # take out proper nouns because they don't really tell us much about the topic and they are another source of noise 
# [x] lemma
     # [x] POS?
# [x] n-grams
# [x] vectorize

import spacy
import numpy as np
from clean_data import news_df
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt



# SpaCy comes with a bunch of pre-built models that tokenize words and also determine if they are alphanumeric, stop words, find their part of speech, lemma, etc.
# SpaCy's lemmatization comes with part of speech tag built in and assigns the corresponding lemma
# With NLTK, you have to specify the POS tag in the WordNet or else some things aren't lemmatized correctly
# SpaCy automatically converts words to lower case
# From the SpaCy documentation about how their tokenizer works:
    # "After consuming a prefix or suffix, we consult the special cases again. 
    # We want the special cases to handle things like “don’t” in English, and we 
    # want the same rule to work for “(don’t)!“. We do this by splitting off the 
    # open bracket, then the exclamation, then the close bracket, and finally 
    # matching the special case"


# Initialize spacy with the english model
sp = spacy.load('en_core_web_sm')
# sp = spacy.load('en', disable=['parser', 'ner'])

@lru_cache(maxsize=None)
def clean_string(text_string):
    '''
    A function to clean a string using SpaCy, removing stop-words, non-alphanumeric characters, and pronouns

    Argument: a text string
    Output: a cleaned string

    '''

    # Parse the text string using the english model initialized earlier
    doc = sp(text_string)
    
    # Initialize empty string
    clean = []

    # Add each token to the list if it is not a stop word, is alphanumeric, and if it's not a pronoun
    for token in doc:
        
        if token.is_alpha == False or token.is_stop == True or token.lemma_ == '-PRON-':
            pass
        else:
            clean.append(token.lemma_)

    # Join the list into a string
    clean = " ".join(clean)

    return clean


def clean_content(df):
    '''
    A function to clean all the strings in a whole of a corpus

    Argument: a dataframe with the column 'content'
    Ouput: same dataframe with a new 'cleaned_content' column
    '''

    # Initialize list of cleaned content strings
    clean_content= []

    # Call clean_string() for each row in the data frame and append to clean_content list
    for row in df.content:

        clean_content.append(clean_string(row))

    # Append clean_content list to the data frame
    df['clean_content'] = clean_content

    return df 

news_df = clean_content(news_df)


if __name__ == '__main__':
    example = news_df.loc[1,'content']

    doc = sp(example)

    for token in doc[0:50]:
        print('%s, %s, %s, %s,' % (token.text, token.lemma_, token.is_alpha, token.is_stop))
    
    example_clean = clean_string(example)
    example
    example_clean

    # This doesn't seem to be doing a good job, ie, labeling mathematical concepts as nationalities etc.
    for entity in doc.ents:
            print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))

# Bag-of-words representation: how many times does each word appear in a document. CountVectorizer creates a bag-of-words by createing a matrix where each feature is a word in the vocabulary and each row is the frequency in each document
# Instead of doing a pure count, you can also scale the feature based on the it's relative frequency. If a word appears a lot in some documents but not in most, it is likely to be informative; if it appears often in most documents, it likely isn't.
# Can do this by vectorizing vocabulary with tf-idf vectorizer (term-frequency inverse-document-frequency)
# Also applies L2 regularization, which makes it so that the length of the document does not change the representation

# Cut back on tokens by using only those that appear in more than 5 documents
# For unsupervized learning, sklearn recommends taking out common words, so I took out words that appear in more than a 15% of documents

vectorizer = TfidfVectorizer(analyzer = 'word', min_df = 5, ngram_range = (1,3), max_df = 0.15)

# Returns the sparse tf-idf weighted document-term matrix
if __name__ == '__main__':
    X = vectorizer.fit_transform(news_df['clean_content'])
    X.shape

# tf-idf is an unsupervised technique that is meant to determine which words distinguished documents 
# to get that matrix, it multiples the idf (inverse document frequency) vector, which gives scores that appear more frequently accorss documents lower scores because they are deemed to be less important, 
# by the document term frequency

# We can inspect which words tf-idf found most important 

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
    terms = vectorizer.get_feature_names() # get the list of terms in the vocabulary
    tfidf = X.todense() # Make the matrix dense 
    tfidf_max = np.array(tfidf.max(axis = 0)).ravel() # get the max tfidf weight of each term and flatten to a 1D array
    plot_tfidf_word_cloud()
    plot_tfidf_word_cloud(most_frequent = False)


# Lower scores mean less informative, higher mean more

