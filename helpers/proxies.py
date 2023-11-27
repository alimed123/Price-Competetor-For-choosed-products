import csv
import random
import os
import os.path
import logging

def get_proxies():

  directory = os.path.dirname(os.path.realpath(__file__))
  proxy_list = []

  with open(f'{directory}/proxy_list.csv', encoding='unicode_escape') as f:

    reader = csv.DictReader(f)

    for line in reader:

      try:
        
        proxy = {}

        protocol = line['protocols']
        ip = line['ip']
        port = line['port']

        proxy_value = f"{ip}:{port}"

        proxy[protocol] = proxy_value

        proxy_list.append(proxy)

      except:
        pass

  # return a random proxy
  rand_prox = random.randint(1, len(proxy_list) - 1)

  random_proxy = proxy_list[rand_prox]

  logging.info('Using proxy: %s', proxy_list[rand_prox])

  return random_proxy

# if __name__ == '__main__':
#   get_proxies()
