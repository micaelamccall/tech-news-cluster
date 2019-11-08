import os
from tech_news_cluster.settings import *
from tech_news_cluster.scrape_news.scrape_news.spiders.spiders import *
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

# Create a directory for data if it doesnt exist
if not os.path.isdir(DATA_PATH):  
    os.makedirs(DATA_PATH)
os.environ['SCRAPY_SETTINGS_MODULE'] = 'tech_news_cluster.scrape_news.scrape_news.settings'
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings=get_project_settings()
process = CrawlerProcess(settings)
process.crawl(VoxSpider)
process.start()
process.stop()

class Scraper:
    def __init__(self):
        self.process = CrawlerProcess(settings=get_project_settings())
        self.spider = VoxSpider    


def get_csv_filenaes:
    CSV_EXPORT_FILE = []
    for pub in PUBLICATIONS:
        CSV_EXPORT_FILE = CSV_EXPORT_FILES.append(pub + ".csv")
        



