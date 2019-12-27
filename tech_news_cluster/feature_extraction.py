# [x] stopwords
# [x] proper nouns
    # take out proper nouns because they don't really tell us much about the topic and they are another source of noise 
# [x] lemma
     # [x] POS?
# [x] n-grams
# [x] vectorize

import spacy
import nltk
import numpy as np
from clean_data import news_df
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer





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

@lru_cache()
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
    clean_content= []

    for row in df.content:

        clean_content.append(clean_string(row))

    df['clean_content'] = clean_content

    return df 

news_df = clean_content(news_df)


if __name__ == '__main__':
    test = news_df.loc[1,'content']

    for token in doc[0:50]:
        print('%s, %s, %s, %s,' % (token.text, token.lemma_, token.is_alpha, token.is_stop))
    
    clean = clean_string(test)
    test
    clean

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
X = vectorizer.fit_transform(news_df['clean_content'])
X.shape

# Make the matrix dense and create a dataframe for later use
tfidf = X.todense()
tfidf_df = pd.DataFrame(tfidf, columns = vectorizer.get_feature_names())

# Plot word cloud of words with highest and lowest tf idf scores like in BESBES or the sklearn book
# Lower scores mean less informative, higher mean more

