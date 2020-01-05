from tech_news_cluster.feature_extraction import clean_string, vectorizer
from tech_news_cluster.kmeans import kmeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def predict(input_string):
    '''
    A function to clean, vectorize, and predict the kmeans cluster of a new string
    
    Arguments: a string, which is the content of an article
    
    Output: a prediction and wordcloud for the document
    '''
    # Clean the string
    clean = clean_string(input_string)
    
    # Vectorize the string
    Y = vectorizer.transform(clean)
    
    # Predict the cluster label
    prediction = kmeans.predict(Y)
    
    # Generate the wordcloud
    cloud = WordCloud().generate(clean)
    
    # Add the prediction to the title of the word cloud
    title = "Document prediction: Cluster {}".format(prediction)
    
    # Show the word cloud
    plt.figure(figsize = [15,20])
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, size =20)
    plt.show();
    

