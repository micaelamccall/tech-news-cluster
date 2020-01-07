from settings import PROJ_ROOT_DIR
import streamlit as st
import pandas as pd
import numpy as np
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt


import spacy

@st.cache(allow_output_mutation= True)
def load_model(name):
    return spacy.load(name)


sp = load_model('en_core_web_sm')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans, KMeans




# @st.cache(allow_output_mutation= True)
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


# @st.cache(allow_output_mutation= True)
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


from clean_data import news_df

news_df = clean_content(news_df)

@st.cache
def vectorize_training_data():
    vectorizer = TfidfVectorizer(analyzer = 'word', min_df = 5, ngram_range = (1,3), max_df = 0.15)
    X = vectorizer.fit_transform(news_df['clean_content'])
    
    returns = (vectorizer, X)

    return returns

vectorizer, X = vectorize_training_data()


@st.cache
def run_kmeans():
    kmeans =  KMeans(n_clusters = 14, init = 'k-means++', random_state= 42)

    cluster_labels = kmeans.fit_predict(X)

    returns = (kmeans, cluster_labels)

    return returns

kmeans, cluster_labels = run_kmeans()

k = 14
terms = vectorizer.get_feature_names()

@st.cache
def print_word_cloud_per_cluster():
    sorted_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    j = 2
    while j < k:
        f, axs = plt.subplots(1,2, figsize = [15, 5])
        
        # for each of the two axes, create a word cloud for that cluster's most important terms, and display it
        for ax, i in zip(axs, range(j-2, j)):
            cloud = WordCloud().generate(text=(' '.join(np.array(terms)[sorted_centroids[i, :75]])))
            title = "Important Words in Cluster {}".format(i)

            ax.imshow(cloud, interpolation="bilinear")
            ax.set_title(title, size = 20)
            ax.grid(False)
            ax.axis("off")
            
            # update j for next loop
            j=j+1
        
        plt.show()

print_word_cloud_per_cluster()

# @st.cache(allow_output_mutation=True)
def predict(input_string = None, filename = None):
    '''
    A function to clean, vectorize, and predict the kmeans cluster of a new string
    
    Arguments: a string, which is the content of an article
    
    Output: a prediction and wordcloud for the document
    '''
    if filename != None:
        with open(os.path.join(PROJ_ROOT_DIR, "content_to_predict", filename), 'r') as file:
            input_string = file.read()
        print('Processing file')
        # Clean the string
        clean = clean_string(input_string)
    
    if input_string != None:
        print('Processing text string')
        clean = clean_string(input_string)
    
    print('String has been cleaned')

    # Vectorize the string
    Y = vectorizer.transform([clean])
    
    print('String has been vectorized')

    # Predict the cluster label
    prediction = kmeans.predict(Y)
    
    # Generate the wordcloud
    cloud = WordCloud().generate(clean)
    
    # Add the prediction to the title of the word cloud
    title = "Cluster Prediction for Article {}".format(prediction)
    
    # Show the word cloud
    plt.figure(figsize = [15,20])
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, size =20)
    plt.show();
    

input_string = st.text_area("Article content")

# st.title("Dogs all over the world")

predict(input_string)