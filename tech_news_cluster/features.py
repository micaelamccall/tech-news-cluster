# [x] stopwords
# [x] proper nouns
    # take out proper nouns because they don't really tell us much about the topic and they are another source of noise 
# [x] lemma
     # [x] POS?
# [] n-grams
# [] vectorize

import spacy
import nltk
from clean_data import news_df

sp = spacy.load('en_core_web_sm')
sp = spacy.load('en', disable=['parser', 'ner'])




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


def clean_string(text_string):
    doc = sp(text_string)
    
    clean = []
    for token in doc:
        
        if token.is_alpha == False or token.is_stop == True or token.lemma_ == '-PRON-':
            pass
        else:
            clean.append(token.lemma_)


    clean = " ".join(clean)

    return clean

def clean_content():

    clean_content= []

    for row in news_df.content:

        clean_content.append(clean_string(row))

    news_df['clean_content']= clean_content

clean_content()


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







