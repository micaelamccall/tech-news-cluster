import os
from tech_news_cluster.settings import PUBLICATIONS
from scrape_news.scrape_news.spiders.spiders import *
from scrape_news.scrape_news.spiders.js_spiders import *
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


# os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
# settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
# settings = get_project_settings()


# process = CrawlerProcess(settings)
# process.crawl(VoxSpider)
# process.start()


class Scraper:
    def __init__(self):
        # set scrapy settings variable to my settings file
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        settings = get_project_settings()
        # Initialize crawler with these settings
        self.process = CrawlerProcess(settings)
    def run_spiders(self):
        # Crawl a spider for each publication set in settings
        for pub in PUBLICATIONS:
            spider = eval(pub + "Spider")
            self.process.crawl(spider)
        # Start the process
        self.process.start()

# Initialize and run the spiders
scraper = Scraper()     
scraper.run_spiders()
        