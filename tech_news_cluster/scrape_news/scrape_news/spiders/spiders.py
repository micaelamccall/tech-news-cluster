import scrapy
from datetime import datetime
import re
from scrape_news.scrape_news.items import ScrapeNewsItem

class ViceSpider(scrapy.Spider):
    name = "vice_spider"

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
        item['title'] = response.xpath("//div[contains(@class, 'article-heading-v2 short-form-v2__heading m-t-4--xs m-b-4--xs')]//h1[contains(@class, 'heading ff--hed lh--hed fw--bold fs--normal size--2 article-heading-v2__title m-t-3--xs m-b-3--xs size--1-md')]/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class, 'article-heading-v2__contributors-rest m-t-2--xs')]//div[contains(@class, 'article-heading-v2__formatted-date dsp-inline--xs')]/descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = response.xpath("//div[contains(@class, 'article-heading-v2__header-dek-wrapper')]//h2/descendant::text()").extract()[0]

        # Getting author
        item['author'] = response.xpath("//div[contains(@class, 'article-heading-v2__contributions ff--body size--5 lh--body')]//a[contains(@class, 'contributor__link bb--link fw--bold')]/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = response.xpath("//a[contains(@class, 'dsp-block--xs lh--tight')]/descendant::text()").extract()[0].title()

        # Get content
        content_list = response.xpath("//div[contains(@data-type, 'body-text')]/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item

class WiredSpider(scrapy.Spider):
    name = "wired_spider"

    # Start URLs
    start_urls = ["https://www.wired.com/category/business/artificial-intelligence/page/1/"]

    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages+10):
        start_urls.append("https://www.wired.com/category/business/artificial-intelligence/page/"+str(i)+"/")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class,'archive-item-component__info')]/a[contains(@class, 'archive-item-component__link')]//@href"):
            url = "https://www.wired.com/" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class,'content-header__row content-header__title-block')]/h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class,'content-header__rubric-date-block')]//time/descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = response.xpath("//div[contains(@class,'content-header__row content-header__accreditation')]//p[contains(@class, 'content-header__row content-header__dek')]/descendant::text()").extract()[0]

        # Getting author
        item['author'] = ''.join(response.xpath("//div[contains(@class,'content-header__rubric-block')]//div[contains(@class, 'bylines bylines--inlined-with-bg')]/descendant::text()").extract())

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = response.xpath("//picture[contains(@class,'responsive-image standard-navigation__logo-image')]//img/@alt").extract()[0].title()

        # Get content
        content_list = response.xpath("//div[contains(@class,'grid--item body body__container article__body grid-layout__content')]//p/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item
