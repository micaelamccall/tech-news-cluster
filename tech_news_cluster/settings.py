import os
import sys


PUBLICATIONS = [
    "Vox",
    # "NYTtimes"
]

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

DATA_PATH = os.path.join(PROJ_ROOT_DIR, "data")

# Create a directory for data if it doesnt exist
if not os.path.isdir(DATA_PATH):  
    os.makedirs(DATA_PATH)


BOT_NAME = 'scrape_news'

SPIDER_MODULES = ['scrape_news.scrape_news.spiders']
NEWSPIDER_MODULE = 'scrape_news.spiders'

FEED_FORMAT = 'csv'
FEED_URI = os.path.join(DATA_PATH, '%(name)s.csv')

ROBOTSTXT_OBEY = True

