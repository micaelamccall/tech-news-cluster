import scrapy
from datetime import datetime
import re
from scrape_news.scrape_news.items import ScrapeNewsItem

class VoxSpider(scrapy.Spider):
    name = "vox_spider"

    # Start URLs
    start_urls = ["https://www.vice.com/en_us/topic/programming?page=1"]

    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages+10):
        start_urls.append("https://www.vice.com/en_us/topic/programming?page="+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'topics-card__content-text')]/a[contains(@class, 'topics-card__heading-link')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class, 'article-heading-v2 short-form-v2__heading m-t-4--xs m-b-4--xs')]/descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = response.xpath("//div[contains(@class, 'article-heading-v2 short-form-v2__heading m-t-4--xs m-b-4--xs')]/descendant::text()").extract()[1]

        # Getting author
        item['author'] = response.xpath("//div[contains(@class, 'article-heading-v2 short-form-v2__heading m-t-4--xs m-b-4--xs')]/descendant::text()").extract()[4]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = response.xpath("//a[contains(@class, 'dsp-block--xs lh--tight')]/descendant::text()").extract()[0].title()

        # Get content
        content_list = response.xpath("//div[contains(@data-type, 'body-text')]/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item

