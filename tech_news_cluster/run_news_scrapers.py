import os
from settings import *
from scrape_news.scrape_news.spiders.spiders import *
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
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        settings = get_project_settings()
        self.process = CrawlerProcess(settings)
    def run_spiders(self):
        for pub in PUBLICATIONS:
            spider = eval(pub + "Spider")
            self.process.crawl(spider)
        self.process.start()


scraper = Scraper()     
scraper.run_spiders()
        