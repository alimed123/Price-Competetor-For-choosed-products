from usp.tree import sitemap_tree_for_homepage
import logging

tree = sitemap_tree_for_homepage('https://www.kayaks2fish.com/')
# logging.info('%s'. tree)

# Check the sitemap status
for subsitemaps in tree.sub_sitemaps:
  status = type(subsitemaps).__name__
  logging.info('\%s is %s status.', subsitemaps.url, status)

counter = 0

# all_pages() returns an Iterator
for page in tree.all_pages():
  counter = counter + 1
  logging.info('%s', page.url)

logging.info('Found %s urls.', counter)