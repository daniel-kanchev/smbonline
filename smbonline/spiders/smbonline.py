import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from smbonline.items import Article


class smbonlineSpider(scrapy.Spider):
    name = 'smbonline'
    start_urls = ['https://www.smbonline.com/blog/index.php']

    def parse(self, response):
        links = response.xpath('//a[@class="btnOrange"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="blogPostTitle"]/text()[2]').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@id="blogContent"]/p/text()[2]').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@id="blogContent"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[2:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
