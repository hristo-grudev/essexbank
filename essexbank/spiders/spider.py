import scrapy

from scrapy.loader import ItemLoader

from ..items import EssexbankItem
from itemloaders.processors import TakeFirst


class EssexbankSpider(scrapy.Spider):
	name = 'essexbank'
	start_urls = ['https://www.essexbank.com/about/blog/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn read"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="page-title"]/text()').get()
		description = response.xpath('//div[@class="l-content"]//text()[normalize-space() and not(ancestor::h1 | ancestor::h4)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="l-content"]//h4/text()').get()

		item = ItemLoader(item=EssexbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
