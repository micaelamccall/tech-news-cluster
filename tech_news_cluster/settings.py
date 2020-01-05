import os
import sys


# Project directory settings
def make_proj_module():
    """
    Sets the root directory of the project, 
    Tells python to check in this directory for modules
    """
    print("Verifying current working directory, which is: " + str(os.getcwd()))
    
    PROJ_ROOT_DIR = os.getcwd()

    if PROJ_ROOT_DIR.find('tech-news-cluster/tech_news_cluster') == -1:
        print('Appending project directory to the current working directory...')
        PROJ_ROOT_DIR = os.path.join(PROJ_ROOT_DIR, "tech_news_cluster")
    else:
        if PROJ_ROOT_DIR.find('tech-news-cluster/tech_news_cluster') != 44:
            print("Incorrect project directory, pls take a closer look")    

    # Tells python to check in this directory for modules
    if not PROJ_ROOT_DIR in sys.path:
        print("Telling python to check for modules in the project directory...")
        sys.path.append(os.path.abspath(PROJ_ROOT_DIR))
    else:
        print("Python is checking for modules in this directory")

    return PROJ_ROOT_DIR

PROJ_ROOT_DIR=make_proj_module()


# Data directory (and setting one if it doesnt exist)
DATA_PATH = os.path.join(PROJ_ROOT_DIR, "data")

if not os.path.isdir(DATA_PATH):  
    os.makedirs(DATA_PATH)


# Webscraping settings

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

ROBOTSTXT_OBEY = True

# Publication to scrape. Comment out to not scrape when running 'run_news_scrape.py'
PUBLICATIONS = [
    # "Vox",
    "Vice",
    "Wired",
    # "NYTimes",
    "WaPo",
    # "Atlantic",
    # "Buzzfeed",
    "Gradient"
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

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
#    'scrape_news.middlewares.ScrapeNewsDownloaderMiddleware': 543,
}

# Setting for scrapy-splash
SPLASH_URL = 'http://0.0.0.0:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}