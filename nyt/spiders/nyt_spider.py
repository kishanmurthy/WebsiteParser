import re
from pathlib import Path
from urllib.parse import urlparse

import scrapy


class NytSpider(scrapy.Spider):
    name = 'nyt'
    allowed_domains = ['wsj.com']
    start_urls = [
        'https://www.wsj.com/'
    ]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)  

    def parse(self, response):
        
        response_content_type = response.headers.get("Content-Type").decode()

        if re.search("(text\/html.*|application\/msword.*|application\/pdf.*|image\/.*)", response_content_type.lower()):
            html_type = re.search("text\/html.*", response_content_type.lower())

            if html_type:
                all_raw_urls = response.css("a::attr(href)").getall() +\
                    response.css("area::attr(href)").getall() +\
                    response.css("img::attr(src)").getall() +\
                    response.css("iframe::attr(src)").getall() +\
                    response.css("frame::attr(src)").getall()
            else:
                all_raw_urls = []



            with open('results/visit_nytimes.csv', 'a') as f:
                f.write(f'{response.url.replace(",","_")},{response.headers.get("Content-Length").decode()},{len(all_raw_urls)},{response_content_type}\n')
            

            if html_type:
                full_urls = [response.urljoin(link) for link in all_raw_urls]
                filtered_urls, url_status = self.process_urls(full_urls)
                with open('results/urls_nytimes.csv', 'a') as f:
                    f.write(''.join(url_status))

                yield from response.follow_all(filtered_urls,self.parse)
        

    def process_urls(self, urls):
        url_status = []
        filtered_urls = []
        for link in urls:
            url = urlparse(link)
            if url.netloc in ['www.wsj.com','wsj.com'] and url.scheme in ['http','https']:
                status = 'OK'
                filtered_urls.append(link)
            else:
                status = 'N_OK'
            url_status.append(f"{link.replace(',','_')},{status}\n")

        filtered_urls = list(set(filtered_urls))
        return filtered_urls, url_status