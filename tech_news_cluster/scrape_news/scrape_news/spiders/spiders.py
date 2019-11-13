import scrapy
from datetime import datetime
import re
from scrape_news.scrape_news.items import ScrapeNewsItem

# This file contains vice_spider, nytimes_spider, wired_spider, atlantic_spider, vox_spider

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

class NYTimesSpider(scrapy.Spider):
    name = "nytimes_spider"

    # Start URLs
    start_urls = ["https://www.nytimes.com/section/technology"]

    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages+10):
        start_urls.append("https://www.vice.com/en_us/topic/programming?page="+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//li[contains(@class, 'css-ye6x8s')]//a/@href"):
            url = "https://www.nytimes.com/" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class, 'css-6cn7ki')]//div[contains(@class, 'css-1sojcmr ehdk2mb0')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = ' '.join(response.xpath("//div[contains(@class, 'css-18e8msd epjyd6m0')]//li[contains(@class, 'css-i49r68')]//time/descendant::text()").extract())

        # Getting summary
        item['summary'] = response.xpath("//div[contains(@class, 'css-6cn7ki')]//p[contains(@class, 'css-1npvhc5 e1wiw3jv0')]/descendant::text()").extract()[0]

        # Getting author
        item['author'] = response.xpath("//div[contains(@class, 'css-18e8msd epjyd6m0')]//div[contains(@class, 'css-1baulvz')]//span/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = response.xpath("//div[contains(@class, 'css-10698na e1huz5gh0')]//a/@aria-label").extract()[0][0:14]

        # Get content
        content_list = response.xpath("//section[contains(@name, 'articleBody')]/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item

class AtlanticSpider(scrapy.Spider):
    name = "atlantic_spider"

    # Start URLs
    start_urls = ["https://www.theatlantic.com/technology/"]

    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages+10):
        start_urls.append("https://www.theatlantic.com/technology/?page="+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//li[contains(@class, 'c-most-popular__item')]//h3/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//header[contains(@class, 'c-article-header')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//header[contains(@class, 'c-article-header')]//div[contains@class, 'c-article-meta')]//time/descendant::text()").extract()[0].strip()

        # Getting summary
        item['summary'] = response.xpath("//header[contains(@class, 'c-article-header')]//div[contains(@class, 'c-article-meta')]/p/descendant::text()").extract()[0]

        # Getting author
        item['author'] = response.xpath("//header[contains(@class, 'c-article-header')]//div[contains(@class, 'c-article-meta')]//address//a/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = response.xpath("//li[contains(@class, 'c-nav__item c-nav__item--main c-nav__item--logo')]//a[contains(@class, 'c-nav__link c-nav__link--main c-nav__link--logo c-logo c-logo--nav')]//span/descendant::text()").extract()[0]

        # Get content
        content_list = response.xpath("//section[contains(@class, 'l-article__section s-cms-content')]//p[contains(@dir, 'ltr')]/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item

# class WaPoSpider(scrapy.Spider):
#     name = "wapo_spider"

#     # Start URLs
#     start_urls = ["https://www.washingtonpost.com/news/innovations/"]

#     npages = 10

#     # Getting multiple pages of articles
#     for i in range(2, npages+10):
#         start_urls.append("https://www.theatlantic.com/technology/?page="+str(i)+"")

#     def parse(self, response):
#         for href in response.xpath("//li[contains(@class, 'c-most-popular__item')]//h3/a/@href"):
#             url = href.extract()
#             yield scrapy.Request(url, callback=self.parse_dir_contents)
        
#     def parse_dir_contents(self, response):
#         item = ScrapeNewsItem()

#         # Getting title
#         item['title'] = 

#         # Gettings date
#         item['date'] = 

#         # Getting summary
#         item['summary'] = 

#         # Getting author
#         item['author'] = 

#         # Get URL
#         item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

#         # Get publication
#         item['publication'] = response.xpath("//li[contains(@class, 'c-nav__item c-nav__item--main c-nav__item--logo')]//a[contains(@class, 'c-nav__link c-nav__link--main c-nav__link--logo c-logo c-logo--nav')]//span/descendant::text()").extract()[0]

#         # Get content
#         content_list = response.xpath("//section[contains(@class, 'l-article__section s-cms-content')]//p[contains(@dir, 'ltr')]/descendant::text()").extract()
#         content_list = [content_fragment.strip() for content_fragment in content_list]
#         item['content'] = ' '.join(content_list).strip()

#         yield item


# class BuzzfeedSpider(scrapy.Spider):
#     name = "buzzfeed_spider"

#     # Start URLs
#     start_urls = ["https://www.buzzfeednews.com/section/tech"]

#     npages = 10

#     # Getting multiple pages of articles
#     for i in range(2, npages+10):
#         start_urls.append("https://www.theatlantic.com/technology/?page="+str(i)+"")

#     def parse(self, response):
#         for href in response.xpath("//span[contains(@class, 'newsblock-story-card__info xs-pr1 xs-block')]//a[contains(@class, 'newsblock-story-card__link xs-flex')]//@href"):
#             url = href.extract()
#             yield scrapy.Request(url, callback=self.parse_dir_contents)
        
#     def parse_dir_contents(self, response):
#         item = ScrapeNewsItem()

#         # Getting title
#         item['title'] = 

#         # Gettings date
#         item['date'] = 

#         # Getting summary
#         item['summary'] = 

#         # Getting author
#         item['author'] = 

#         # Get URL
#         item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

#         # Get publication
#         item['publication'] = 

#         # Get content
#         content_list = 
#         content_list = [content_fragment.strip() for content_fragment in content_list]
#         item['content'] = ' '.join(content_list).strip()

#         yield item


class VoxSpider(scrapy.Spider):
    name = "vox_spider"

    # Start URLs
    start_urls = ["https://www.vox.com/future-perfect"]

    npages = 10

    # Getting multiple pages of articles
    for i in range(2, npages+10):
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

