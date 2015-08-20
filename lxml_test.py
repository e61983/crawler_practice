#!/usr/bin/env python
# encoding: utf-8

import requests
from lxml import etree
from os.path import exists

url = 'http://clbc.tw/'
cache_path = 'cache.html'

def save(url, path = None):
    if not path:
        path = basename(url)
    with open(path, 'w') as f:
        f.write(requests.get(url).content)


def get(url, path = None):
    if exists(path):
        with open(path, 'r') as f:
            content = f.read()
    else:
        content = requests.get(url).content
        with open(path,'w') as f:
            f.write(content)
    return content

root = etree.HTML(get(url, cache_path))
head = root.find('head')
print head
head_children = head.getchildren()
print head_children
metas = head.findall('meta')
print metas
title_text = head.findtext('title')
print title_text
