from settings import PROJ_ROOT_DIR, DATA_PATH

import pandas as pd
import os
import datetime
from functools import lru_cache
import spacy


def load_news_data():
    """
    A function to load scraped news data from data folder
    """

    files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]
    file_list = []
    for filename in files:
        df = pd.read_csv(os.path.join(DATA_PATH, filename))
        file_list.append(df)
    df_full = pd.concat(file_list, join='outer').drop_duplicates().reset_index().drop(columns='index')
    return df_full


news_df = load_news_data().dropna(subset=['content'])

if __name__ == '__main__':
    # Number of news articles from each publication 
    news_df.publication.value_counts()


    # Look at shape
    news_df.shape
    # Check format of date for each publication
    for pub in news_df['publication'].unique():
        print(pub, news_df[news_df.publication==pub].date.iloc[0])



def process_date_feature(df=news_df):
    """
    A function to process the various dates into a consistant isformate
    """

    news_df = df

    # Take out the time from the date columns by replacing the dates in publications that have time included without the time
    repl_dict = {}
    for row in news_df.itertuples():
        if row.publication== 'Vox':
            repl_dict[row.date] = row.date[0:-13]
        elif row.publication == 'Vice':
            repl_dict[row.date] =row.date[0:-8].strip()
        elif row.publication == 'Buzzfeed News':
            if row.date.find('Posted on') == 0:
                repl_dict[row.date] = row.date[10:-16].strip()
            elif row.date.find('Last updated on') == 0:
                repl_dict[row.date] = row.date[16:-17].strip()
            else:
                repl_dict[row.date] = row.date[:-11].strip()
        elif row.publication == 'WashingtonPost':
            repl_dict[row.date] = row.date[:-16].strip()
        else:
            repl_dict[row.date] = str(row.date).strip()

    news_df.date = news_df.date.replace(repl_dict)

    # If any dates end with a comma, take that out
    repl_dict = {}
    for row in news_df.itertuples():
        if str(row.date).endswith(','):
            repl_dict[row.date] = row.date[:-1]
        else:
            repl_dict[row.date] = str(row.date).strip()

    news_df.date = news_df.date.replace(repl_dict)

    # Separate the year and daymonth from the date strings
    year = []
    daymonth = []
    for row in news_df.itertuples():
        if row.publication == 'Wired':
            year.append('20' + str(row.date)[-2:])
            daymonth.append(str(row.date[:-3]))
        else:
            year.append(str(row.date)[-4:])
            daymonth.append(str(row.date)[:-4].strip())
            
    # Append year and daymonth columns
    news_df['year'] = year
    news_df['daymonth'] = daymonth

    news_df.year.value_counts()
    news_df.daymonth.value_counts()

    del(year, daymonth)

    # If any daymonths end with a comma, take that out
    repl_dict = {}
    for row in news_df.itertuples():
        if str(row.daymonth).strip().endswith(','):
            repl_dict[row.daymonth] = row.daymonth.strip()[:-1]
        else:
            repl_dict[row.daymonth] = str(row.daymonth).strip()

    news_df.daymonth = news_df.daymonth.replace(repl_dict)

    # Separate out day and month
    day = []
    month = []
    for row in news_df.itertuples():
        if row.publication == 'The Gradient':
            day.append(str(row.daymonth)[:2])
            month.append(str(row.daymonth[-4:-1]))
        elif row.publication == 'Wired':
            day.append(str(row.daymonth)[-2:].strip())
            month.append(str(row.daymonth)[:-3].strip())
        else:
            day.append(str(row.daymonth)[-2:].strip())
            month.append(str(row.daymonth).strip()[:-2])
            
    # Append day and month columns
    news_df['day'] = day
    news_df['month'] = month

    news_df=news_df.drop(columns = ['daymonth'])

    del(day, month)

    # If any months end with a comma, take that out
    repl_dict = {}
    for row in news_df.itertuples():
        if str(row.month).strip().endswith('.'):
            repl_dict[row.month] = row.month.strip()[:-1]
        else:
            repl_dict[row.month] = str(row.month).strip()

    news_df.month = news_df.month.replace(repl_dict)

    # Replace string months with int months
    repl_dict = {
        'May':'05',
        'Jun':'06', 'June':'06', 
        'Jul': '07', 'July':'07', 
        'Aug':'08', 'August': '08', 
        'Sep': '11', 'September': '11', 
        'Oct': '10', 'October': '10', 
        'Nov':'11', 'November': '11', 
        'Dec': '12', 'December': '12', 
        'Jan':'01', 'January':'01', 
        'Feb':'02', 'February':'02', 
        'Mar': '03', 'March': '03', 
        'Apr':'04', 'April':'04'}

    news_df.month = news_df.month.replace(repl_dict)

    # Add a 0 to the beginning of any single digit months remianing 
    repl_dict = {}
    for row in news_df.itertuples():
        if len(str(row.day).strip()) < 2:
            repl_dict[row.day] = '0' + row.day.strip()
        else:
            repl_dict[row.day] = str(row.day).strip()

    news_df.day = news_df.day.replace(repl_dict)

    news_df.month.value_counts()

    # Change date column to isoformat
    isoformat = []
    for row in news_df.itertuples():
        try:
            isoformat.append(datetime.date(int(row.year), int(row.month), int(row.day)).isoformat())
        except ValueError:
            isoformat.append('NA')

    news_df.date=isoformat

    return news_df

news_df = process_date_feature()


if __name__ == '__main__':
    for col in news_df:
        print(col, type(col))


# [x] stopwords
# [x] proper nouns
    # take out proper nouns because they don't really tell us much about the topic and they are another source of noise 
# [x] lemma
     # [x] POS?
# [x] n-grams
# [x] vectorize



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


# Perform content cleaning
if __name__ == '__main__':
    news_df = clean_content(news_df)
    news_df.to_csv('tech_news_cluster/data/clean_content.csv')

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

