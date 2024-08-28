import scrapy
import json
import os
import time

class WebFoundationSpider(scrapy.Spider):
    name = 'ogbv'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_South_African_slang_words']

    def parse(self, response):
        paragraphs = response.css('p::text').getall()
        italics = response.css('i::text').getall()
        headings = response.css('h1::text, h2::text, h3::text').getall()
        lists = response.css('ul li::text, ol li::text').getall()
        links = response.css('a::attr(href)').getall()
        images = response.css('img::attr(src)').getall()
        metadata = {
            'title': response.css('title::text').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'meta_keywords': response.css('meta[name="keywords"]::attr(content)').get()
        }

        data = {
            'paragraphs': [p.strip() for p in paragraphs if p.strip()],
            'italics': [i.strip() for i in italics if i.strip()],
            'headings': [h.strip() for h in headings if h.strip()],
            'lists': [li.strip() for li in lists if li.strip()],
            'links': links,
            'images': images,
            'metadata': metadata
        }

        self.log(f'Data extracted: {data}')
        self.save_to_file(data)

    def save_to_file(self, data):
        self.log(f'Attempting to save data: {data}')
        file_name = f'data_{int(time.time())}.json'
        file_path = os.path.join('.','.', file_name)
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            self.log('Successfully saved data to data.json')
        except IOError as e:
            self.log(f'Error saving data to data.json: {e}')
