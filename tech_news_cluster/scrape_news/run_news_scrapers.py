import os
from settings import *
from scrape_news.scrape_news.spiders.spiders import *
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

# Create a directory for data if it doesnt exist
# if not os.path.isdir(DATA_PATH):  
#     os.makedirs(DATA_PATH)




process = CrawlerProcess(settings)
process.crawl(VoxSpider)



class Scraper:
    def __init__(self):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'scrape_news.scrape_news.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        settings = get_project_settings()
        self.process = CrawlerProcess(settings)
    def run_spiders(self):
        for pub in PUBLICATIONS:
            spider = pub + "Spider"
            csv_file = os.path.join(DATA_PATH, str(pub.lower()) + ".csv")
            self.process.crawl(spider)
        self.process.start()


scraper = Scraper()     
scraper.run_spiders()
        

        


def get_csv_filenaes:
    CSV_EXPORT_FILE = []
    for pub in PUBLICATIONS:
        CSV_EXPORT_FILE = CSV_EXPORT_FILES.append(pub + ".csv")
        


process.start()
