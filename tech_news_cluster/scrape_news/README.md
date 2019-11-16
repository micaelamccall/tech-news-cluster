For this project, I wanted to scrape news articles from a few of the news sites I spend time on. Because I'm interested especially in categories in "tech" or "future", I wanted to scrape these articles directly from these pages. 

I like using Scrapy because of how easy it is to make modular scraping projects, structure scraped data, save to CSVs, and call spiders from different scripts. 

I ran into some problems with some news sites using JavaScript to dynamically render a list of news articles in a section (rather than pressing a 'next' button and getting a URL). While this latter case has some really good [tutorials](https://towardsdatascience.com/using-scrapy-to-build-your-own-dataset-64ea2d7d4673) to deal with this situation, I had a harder time discovering the best way to scrape the JavaScript rendered pages. 

Splash is available as a spider image 