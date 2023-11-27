from lxml import etree
from io import BytesIO
import requests
import gzip
import logging

r = requests.get('https://www.kayaks2fish.com/sitemap_1.xml.gz')
sitemap = gzip.GzipFile(fileobj=BytesIO(r.content)).read()

root = etree.fromstring(sitemap)

for url in root.xpath("//xmlns:loc/text()", namespaces={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"}):
  logging.info('%s', url)
