import scrapy
from datetime import datetime
import re
from scrape_news.scrape_news.items import ScrapeNewsItem
# from scrape_news.items import ScrapeNewsItem
from scrapy_splash import SplashRequest


class WaPoSpider(scrapy.Spider):
    name = "wapo_spider"

    # Start URLs
    start_urls = ["https://www.washingtonpost.com/news/innovations/"]
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    # # Script to click on 'show more' button
    # script = """
    #     function main(splash, args)
    #         assert(splash:go(splash.args.url))
    #         splash:set_user_agent(user_agent)
    #         splash:wait(0.5)
    #         local element = splash:select('div.pb-loadmore-div-ans')
    #         local bounds = element:bounds()
    #         element:mouse_click{x=bounds.width/2, y=bounds.height/2}
    #         splash:wait(2)
    #         return splash:html()
    #     end
    # """


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.parse, endpoint= 'execute', args={'lua_source': self.script})

    
    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'story-headline')]//h2/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//div[contains(@class, 'w-100')]//h1/descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//div[contains(@class, 'display-date')]//descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = 'NA'

        # Getting author
        item['author'] = response.xpath("//a[contains(@class, 'author-name')]//descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'WashingtonPost'

        # Get content
        content_list = response.xpath("//div[contains(@class, 'article-body')]//p/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item


class NYTimesSpider(scrapy.Spider):
    name = "nytimes_spider"


    # Start URLs
    start_urls = ["https://www.nytimes.com/section/technology"]
    

    # Script to click on 'show more' button
    script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            splash:wait(0.5)
            local element = splash:select('div.css-1stvaey button')
            local bounds = element:bounds()
            element:mouse_click{x=bounds.width/2, y=bounds.height/2}
            splash:wait(2)
            local elementt = splash:select('div.css-1stvaey button')
            local boundss = elementt.bounds()
            elementt:mouse_click{x=boundss.width/2, y=boundss.height/2}
            splash:wait(2)
            local elementtt = splash:select('div.css-1stvaey button')
            local boundsss = elementtt.bounds()
            elementtt:mouse_click{x=boundsss.width/2, y=boundsss.height/2}
            splash:wait(2)
            return splash:html()
        end
    """


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint= 'execute', args={'lua_source': self.script})

    
    def parse(self, response):
        for href in response.xpath("//li[contains(@class, 'css-ye6x8s')]//a/@href"):
            url = "https://www.nytimes.com/" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self, response):
        item = ScrapeNewsItem()

        # Getting title
        item['title'] = response.xpath("//h1[contains(@itemprop, 'headline')]//descendant::text()").extract()[0]

        # Gettings date
        item['date'] = response.xpath("//time/descendant::text()").extract()[0]

        # Getting summary
        item['summary'] = 'NA'

        # Getting author
        item['author'] = response.xpath("//p[contains(@itemprop, 'author')]//span[contains(@itemprop, 'name')]/descendant::text()").extract()[0]

        # Get URL
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        # Get publication
        item['publication'] = 'New York Times'

        # Get content
        content_list = response.xpath("//div[contains(@class, 'StoryBody') or contains(@class, 'story-body')]//p/descendant::text()").extract()
        content_list = [content_fragment.strip() for content_fragment in content_list]
        item['content'] = ' '.join(content_list).strip()

        yield item


