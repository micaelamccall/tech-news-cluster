# Scraping news articles

For this project, I wanted to scrape news articles from a few of the news sites I spend time on. Because I'm interested especially in categories in "tech" or "future", I wanted to scrape these articles directly from these pages. 

I like using Scrapy because of how easy it is to make modular scraping projects, structure scraped data, save to CSVs, and call spiders from different scripts. 

I ran into some problems with some news sites using JavaScript to dynamically render a list of news articles in a section (rather than pressing a 'next' button and getting a URL). While this latter case has some really good [tutorials](https://towardsdatascience.com/using-scrapy-to-build-your-own-dataset-64ea2d7d4673) to deal with this situation, I had a harder time discovering the best way to scrape the JavaScript rendered pages. 

I decided to use Splash, a lightweight browser, to render the JavaScript of these websites before scraping them. 

Splash is available as a Docker image pulled from scrapinghub/splash and runs as a conatiner on localhost:8050.

By using scrapy-splash.SplashRequest instead of scrapy.Request, I rendered html versions of JavaScript pages to parse with Scrapy spiders.

Splash also uses Lua scripts to interact with JavaScript elements. SplashRequest executes these scripts and renders the resulting html to be parsed. I wrote a Lua script that clicks on a "load more" button, and returns the html to parse and follow all the loaded article links on the page, which can then be accessed with a normal scrapy.Request. 

All of this happens in a normal scrapy.Spider object, so it can be crawled normally, as long as the Splash Docker image is running in localhost:8050.

