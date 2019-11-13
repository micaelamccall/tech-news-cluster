import os
import sys


# Project directory settings
def set_root_dir():
    """Sets the root directory of the project"""
    print("Verifying current working directory, which is: " + str(os.getcwd()))
    
    PROJ_ROOT_DIR = os.getcwd()

    if PROJ_ROOT_DIR.find('tech-news-cluster/tech_news_cluster') == -1:
        print('Appending project directory to the current working directory...')
        PROJ_ROOT_DIR = os.path.join(PROJ_ROOT_DIR, "tech_news_cluster")
    else:
        if PROJ_ROOT_DIR.find('tech-news-cluster/tech_news_cluster') != 44:
            print("Incorrect project directory, pls take a closer look")    

    return PROJ_ROOT_DIR

PROJ_ROOT_DIR=set_root_dir()

def make_proj_module(project_directory=PROJ_ROOT_DIR):
    """Tells python to check in this directory for modules"""
    if not PROJ_ROOT_DIR in sys.path:
        print("Telling python to check for modules in the project directory...")
        sys.path.append(os.path.abspath(PROJ_ROOT_DIR))
    else:
        print("Python is checking for modules in this directory")

if __name__ == '__main__':
    make_proj_module()


# Data directory (and setting one if it doesnt exist)
DATA_PATH = os.path.join(PROJ_ROOT_DIR, "data")

if not os.path.isdir(DATA_PATH):  
    os.makedirs(DATA_PATH)


# Webscraping settings

ROBOTSTXT_OBEY = True

# Publication to scrape. Comment out to not scrape when running 'run_news_scrape.py'
PUBLICATIONS = [
    "Vox",
    "Vice",
    "Wired",
    # "NYTimes",
    "Atlantic",
    # "Buzzfeed"
]

# Scrapy bot name
BOT_NAME = 'scrape_news'

# Location of scrapy spiders
SPIDER_MODULES = ['scrape_news.scrape_news.spiders']
NEWSPIDER_MODULE = 'scrape_news.spiders'

# Format to save scraped data
FEED_FORMAT = 'csv'

# Location to save scraped data, named according to name of spider
FEED_URI = os.path.join(DATA_PATH, '%(name)s_%(time)s.csv')
