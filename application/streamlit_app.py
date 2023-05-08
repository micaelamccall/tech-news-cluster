from settings import PROJ_ROOT_DIR
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
# import en_core_web_sm


# st.title("How Does Unsupervised Learning Group Tech News Articles?")
st.title("Categorize a Tech Article Based on Unsupervized Clustering")

# st.markdown("![image](/assets/image.jpeg)")
st.image("assets/image.png")

@st.cache_data
def load_model(name):
    return spacy.load(name)

sp = spacy.load("en_core_web_sm")

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


# Load the models

@st.cache_data
def load_model():
    vectorizer = joblib.load('models/tfidf_vectorizer_new.sav')
    kmeans = joblib.load('models/kmeans_new.sav')

    returns = (vectorizer, kmeans)

    return returns

vectorizer, kmeans = load_model()
# vectorizer = joblib.load(open('models/tfidf_vectorizer.sav', "rb"))
# kmeans = joblib.load(open('models/kmeans.sav', "rb"))
# st.write(type(kmeans))

# from predict import vectorizer, kmeans

terms = vectorizer.get_feature_names()
 
k = 15


input_string = st.text_area("Article to Predict", "Paste article content here")

def predict(input_string = None):
    '''
    A function to clean, vectorize, and predict the kmeans cluster of a new string
    
    Arguments: a string, which is the content of an article
    
    Output: a prediction and wordcloud for the document
    '''
    
    if input_string != None:
        clean = clean_string(input_string)

    # Vectorize the string
    Y = vectorizer.transform([clean])

    # Predict the cluster label
    prediction = kmeans.predict(Y)

    returns = (prediction, clean)
    return returns

pred_text = st.empty()


# pred_button = st.button("Predict")

if input_string == 'Paste article content here':
    pass
else:
    prediction, clean = predict(input_string=input_string)
    pred_text = st.title("Article belongs to cluster " + str(list(prediction)[0]))



def print_prediction_cloud(clean, prediction):
    # Generate the wordcloud
    cloud = WordCloud(background_color='white').generate(clean)
    
    # Add the prediction to the title of the word cloud
    # title = "Cluster Prediction for Article {}".format(prediction)
    
    # Show the word cloud
    f = plt.figure()
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    # plt.title(title, size =20)

    return f
    

pred_cloud = st.button("Display WordCloud of Article Text")

if pred_cloud == True:
    prediction, clean = predict(input_string=input_string)
    f = print_prediction_cloud(clean, prediction)
    st.pyplot(f)





# st.markdown('\n \n \n *After cleaning article content and running KMeans on articles from seven news sites, 14 clusters were identified*')

st.image("assets/image2.png")
st.title('So what does that mean? ')
st.subheader('View the most important words in each cluster')

@st.cache_data
def calc_centroids():
    sorted_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    return sorted_centroids

sorted_centroids = calc_centroids()

@st.cache_data
def print_top_words_by_cluster(sorted_centroids, i):
    cluster = "Cluster %d:" % i
    words = []
    for ind in sorted_centroids[i, :14]:
        if terms[ind].find(' ') == -1:
            words.append(terms[ind])
    returns = (cluster, words)
    return returns




def print_word_cloud_per_cluster(j=2):
    
    if j >= k:
        return 
    
    else:
        f, axs = plt.subplots(1,2, figsize = [15, 5])
        
        # for each of the two axes, create a word cloud for that cluster's most important terms, and display it
        for ax, i in zip(axs, range(j-2, j)):
            cloud = WordCloud(background_color='white').generate(text=(' '.join(np.array(terms)[sorted_centroids[i, :75]])))
            title = "Important Words in Cluster {} \n".format(i)

            ax.imshow(cloud, interpolation="bilinear")
            ax.set_title(title, size = 30)
            ax.grid(False)
            ax.axis("off")
        st.pyplot(f)
            
        # update j for next loop
        print_word_cloud_per_cluster(j=j+2)
    
        

# st.pyplot(print_word_cloud_per_cluster())
# st.subheader("View word cloud for top words of each cluster?")
# cluster_cloud = st.checkbox("Display", value = False)

view_option = st.radio("", ("View as list", "View as WordCloud"))


if view_option == "View as WordCloud":
    print_word_cloud_per_cluster()
if view_option == "View as list":
    for i in range(14):
        cluster, words = print_top_words_by_cluster(sorted_centroids, i)
        st.write(cluster, ' '.join(words))



