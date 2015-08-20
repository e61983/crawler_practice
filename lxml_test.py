#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import exists, join
from hashlib import md5
from collections import deque

from lxml import etree
import requests


url = 'http://clbc.tw/'
cache_path = 'cache.html'

def save(url, path = None):
    if not path:
        path = basename(url)
    with open(path, 'w') as f:
        f.write(requests.get(url).content)


def get(url, cache_dir_path = 'cache/'):

    if not exists(cache_dir_path):
        makedirs(cache_dir_path)

    cache_path = join( cache_dir_path, md5(url).hexdigest())
    if exists(cache_path):
        with open(cache_path, 'r') as f:
            content = f.read().decode('utf-8')
    else:
        content = requests.get(url).content
        with open(cache_path,'w') as f:
            f.write(content)
    return content

def find_urls(source_code):
    root = etree.HTML(source_code)
    return [a.attrib['href'] for a in root.xpath('//a') if 'href' in a.attrib]

source_code = get(url)
print find_urls(source_code)
