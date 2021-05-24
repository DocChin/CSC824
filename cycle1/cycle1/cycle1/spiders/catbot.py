import scrapy


class CatbotSpider(scrapy.Spider):
    name = 'catbot'
    allowed_domains = ['www.reddit.com/r/cats/']
    start_urls = ['https://www.reddit.com/r/cats/']


    def parse(self, response):
        #Extracting the content using css selectors
        titles = response.css('title').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
        comments = response.css('.comments::text').extract()
        page = response.url.split("/")[-2]
        filename = f'cats-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        #Give the extracted content row wise
        for item in zip(titles,votes,times,comments):
            #create a dictionary to store the scraped info
            scraped_info = {
                'title' : item[0],
                'vote' : item[1],
                'created_at' : item[2],
                'comments' : item[3],
            }
        
            #yield or give the scraped info to scrapy
            yield scraped_info
