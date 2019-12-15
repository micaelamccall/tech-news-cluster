import scrapy
from datetime import datetime
import re
# from scrape_news.scrape_news.items import ScrapeNewsItem
from scrape_news.items import ScrapeNewsItem

# This file contains vice_spider, buzzfeed_spider, wired_spider, atlantic_spider, vox_spider

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
    for i in range(2, npages):
        start_urls.append("https://www.wired.com/category/business/artificial-intelligence/page/"+str(i)+"/")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class,'archive-item-component__info')]/a[contains(@class, 'archive-item-component__link')]//@href"):
            url = "https://www.wired.com/" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//header[contains(@class,'content-header')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//header[contains(@class,'content-header')]//time/descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = 'NA'

        # Getting author
        item['author'] = ''.join(response.xpath("//header[contains(@class,'content-header')]//span[contains(@class, 'byline-component')]//descendant::text()").extract()[0])

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = "Wired"
        
        # Get content
        content_list = response.xpath("//div[contains(@class,'article-main') or contains(@class, 'article__body')]//p/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item


class AtlanticSpider(scrapy.Spider):
    name = "atlantic_spider"

    # Start URLs
    start_urls = ["https://www.theatlantic.com/technology/"]

    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages):
        start_urls.append("https://www.theatlantic.com/technology/?page="+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//li[contains(@class, 'c-most-popular__item')]//h3/a/@href"):
            # dont crawl video pages
            if not "video" in href.extract():
                url = href.extract()
                yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//header[contains(@class, 'c-article-header')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//header[contains(@class, 'c-article-header')]//div[contains(@class, 'c-article-meta')]//time/descendant::text()").extract()[0].strip()

        # Getting summary
        item['summary'] = response.xpath("//header[contains(@class, 'c-article-header')]//div[contains(@class, 'c-article-meta')]/p/descendant::text()").extract()[0]

        # Getting author
        item['author'] = response.xpath("//header[contains(@class, 'c-article-header')]//div[contains(@class, 'c-article-meta')]//address//a/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'Atlantic'

        # Get content
        content_list = response.xpath("//section[contains(@class, 'l-article__section s-cms-content')]//p[contains(@dir, 'ltr')]/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item


class VoxSpider(scrapy.Spider):
    name = "vox_spider"

    # Start URLs
    start_urls = ["https://www.vox.com/future-perfect"]

    npages = 5

    # Getting multiple pages of articles
    for i in range(2, npages):
        start_urls.append("https://www.vox.com/future-perfect/archives/"+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'c-compact-river__entry')]//a[contains(@class, 'c-entry-box--compact__image-wrapper')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//div[contains(@class, 'c-byline')]//time/descendant::text()").extract()[0].strip()

        # Getting summary
        item['summary'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//p/descendant::text()").extract()[0]

        # Getting author
        item['author'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//div[contains(@class, 'c-byline')]//span[contains(@class, 'c-byline__author-name')]/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'Vox'

        # Get content
        content_list = response.xpath("//div[contains(@class, 'c-entry-content')]//descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item

class BuzzfeedSpider(scrapy.Spider):
    name = "buzzfeed_spider"


    # Start URLs
    start_urls = ["https://www.buzzfeednews.com/section/tech"]


    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages):
        start_urls.append("https://www.buzzfeednews.com/section/tech?page="+str(i)+"")


    def parse(self, response):
        for href in response.xpath("//h2[contains(@class, 'newsblock-story-card__title')]//a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//h1[contains(@class, 'buzz-title') or contains(@class, 'news-article-header')]//descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class, 'buzz-timestamp') or contains(@class, 'timestamps')]//descendant::text()").extract()[1].strip()

        # Getting summary
        item['summary'] = response.xpath("//p[contains(@class, 'buzz-dek') or contains(@class, 'news-article-header__dek')]//descendant::text()").extract()[0].strip()

        # Getting author
        item['author'] = [n.strip() for n in response.xpath("//div[contains(@class, 'byline')]//a//span//descendant::text()").extract() if len(n)>7][0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'Buzzfeed News'

        # Get content
        content_list = response.xpath("//div[contains(@class, 'subbuzz subbuzz-text') or contains(@class, 'subbuzz__description')]/p/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item


class VoxSpider(scrapy.Spider):
    name = "vox_spider"

    # Start URLs
    start_urls = ["https://www.vox.com/future-perfect"]

    npages = 5

    # Getting multiple pages of articles
    for i in range(2, npages):
        start_urls.append("https://www.vox.com/future-perfect/archives/"+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'c-compact-river__entry')]//a[contains(@class, 'c-entry-box--compact__image-wrapper')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//div[contains(@class, 'c-byline')]//time/descendant::text()").extract()[0].strip()

        # Getting summary
        item['summary'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//p/descendant::text()").extract()[0]

        # Getting author
        item['author'] = response.xpath("//div[contains(@class, 'c-entry-hero c-entry-hero--default ')]//div[contains(@class, 'c-byline')]//span[contains(@class, 'c-byline__author-name')]/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'Vox'

        # Get content
        content_list = response.xpath("//div[contains(@class, 'c-entry-content')]//descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item

class GradientSpider(scrapy.Spider):
    name = "gradient_spider"


    # Start URLs
    start_urls = ["https://thegradient.pub/"]


    npages = 4

    # Getting multiple pages of articles
    for i in range(2, npages):
        start_urls.append("https://thegradient.pub/page/"+str(i)+"/")


    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'c-post-card__media')]/a//@href"):
            url = "https://thegradient.pub" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class, 'c-post-hero__content')]/h1//descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class, 'c-post-hero__content')]/time//descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = "NA"

        # Getting author
        item['author'] = response.xpath("//div[contains(@class, 'c-widget c-widget-author')]//h3/a/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'The Gradient'

        # Get content
        content_list = response.xpath("//div[contains(@class, 'c-content')]//div[contains(@class, 'kg-card-markdown')]/p/text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item
