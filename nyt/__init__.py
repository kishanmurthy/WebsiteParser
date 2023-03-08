import logging
from pathlib import Path

from scrapy.utils.log import configure_logging

Path('results').mkdir(parents=True, exist_ok=True)
with open('results/fetch_nytimes.csv', 'w') as f:
    f.write('url,status\n')

with open('results/visit_nytimes.csv', 'w') as f:
    f.write('url,size (bytes),# of outlinks found,content-type\n')

with open('results/urls_nytimes.csv', 'w') as f:
    f.write('url,indicator\n')

logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.ERROR
)
