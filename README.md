# Finding topic clusers in tech news: using unsupervized learning to cluster news articles based on content

*python | webscraping | natural language processing | kmeans | t-sne*

# Intro

It started in July 2019, when I stumbled the phrase that AI poses “an existential threat” to humanity. I didn’t know what that meant at the time: a threat to human existence. For some reason, I found that claim to be satisfyingly bold, and I wanted to know more. Embarking into a clickhole typical of my obsessive nature, I subscribed to some news sites on AI and started reading way more tech news.

In my reading of tech news, I struggled to identify topics or themes that interested me and were worth my time.

While tags can be helpful to get a sense of an article outside of the title, many of them seem to reference vague, poorly defined or refined terms.  Rather than relying on these tags, I wanted to see if unsupervised learning could help me identify themes or groups of themes to assist in my reading. 

## Dataset

I scraped article title, content, date, author, and url were from the tech sections of the following news sites:
- Vox
- Vice
- New York Times
- Wired
- The Atlantic
- BuzzFeed
- The Gradient

By selecting news from sites that don’t specifically focus on tech or science news, I hoped that this idea could be generalized to other vague or broad news topics. 

Code for scraping part of the project is in "scrape_news" directory.

# Project Goals

I aimed to find clusters in tech news articles based on the full content of the article and understand themes or constructs that can summarize the clusters.

# Usage

Project scripts and Jupyter Notebook are in the tech-news-cluster directory

- `tech_news_cluster.ipynb` is the notebook with all the script

- Project scripts
    - `settings.py` makes the project a module, creates the data directory, sets which publications to scrape, settings for scrapy and splash
    - `run_news_scrapers.py` runs the scrapers and saves the it in the data folder
    - `clean_data.py` processes data, leans and lemmatizes content of articles
    - `feature_extraction` runs tf-idf vectorization of content, plots word clouds for vectorized words
    - `kmeans.py` functions to choose the best value of k, train KMeans algorithm, and prints top words per cluster
    - `tSNE.py` 2 dimensional t-SNE plot
    - `predict.py` functions to process and predict cluster label of new strings or files


# Findings

I identfied 15 clusters with the following top terms

Cluster 0: tiktok china chinese huawei hong kong xinjiang camp uighurs beijing internment
Cluster 1: learning openai robot art deep train neural task dataset
Cluster 2: charity tax foundation philanthropy gates donate billionaire kidney donor donation wealth giving
Cluster 3: instagram influencer youtube ad meme follower brand tumblr creator star tweet fan
Cluster 4: patient vaccine nuclear disease outbreak ebola brain weapon egg cancer medical crispr
Cluster 5: climate carbon energy emission fire air pollution gas renewable fuel clean
Cluster 6: apple camera device portal iphone ring airpods store police privacy card headphone
Cluster 7: facial recognition surveillance police camera ban privacy
Cluster 8: meat burger plant beyond impossible foods vegan
Cluster 9: opioid prison drug gun addiction justice crime criminal sackler incarceration purdue
Cluster 10: deepfake election tweet musk zuckerberg fake unsworth court voter whatsapp
Cluster 11: programming python java web javascript programmer command script file variable html
Cluster 12: student college water employee bank parent debt bias academic well
Cluster 13: amazon alexa delivery seller assistant contractor bezos contract privacy driver customer speaker
Cluster 14: income poverty uber cash car tax worker eitc poor driver ubi

