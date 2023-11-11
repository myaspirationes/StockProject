# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/27 11:04
@Auth ： Tiger
@File ：ajax_spider.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""
import requests
import logging
import json
from os import makedirs
from os.path import exists

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'

LIMIT = 10
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
TOTAL_PAGE = 3

RESULTS_DIR = 'results'

# 判断是否存在路径; 如果不存在重新创建一个

exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


def scrape_api(url):
    logging.info('scraping  %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('get  invalid  status  code  %s  while  scraping  %s', response.status_code, url)
    except  requests.RequestException:
        logging.error('error  occurred  while  scraping  %s', url, exc_info=True)


def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


def get_data():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail  data  %s', detail_data)

            save_data(detail_data)


if __name__ == '__main__':
    get_data()
