#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import exists, join
from hashlib import md5
from collections import deque

from lxml import etree
import requests

from PIL import Image
from StringIO import StringIO
import time
import urlparse

def saveImage(url, save_dir_path = 'image/'):
    if not exists(save_dir_path):
        makedirs(save_dir_path)
    save_path = join(save_dir_path,md5(url).hexdigest())
    if not exists(save_path):
        content = requests.get(url).content
        with open(save_path,'wb') as img:
            img.write(content)
    return save_path

def showImage(url, save = False):
    if (save):
        with open(saveImage(url),'rb') as file:
            img = Image.open(file)
            img.show()
    else:
        file = requests.get(url).content
        img = Image.open(StringIO(file))
        img.show()
        file.close()

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

def to_Abs_link(base, url):
    if not url.startswith('http://'):
        return urlparse.urljoin(base, url)
    else:
        return url

def find_urls(base, source_code):
    root = etree.HTML(source_code)
    return  [to_Abs_link(base,a.attrib['href']) for a in root.xpath('//a') if 'href' in a.attrib]

def find_url_image(base, source_code):
    root = etree.HTML(source_code)
    return  [to_Abs_link(base,a.attrib['src']) for a in root.xpath('//img') if 'src' in a.attrib]

def search_Beauty(url):
    url_queue=deque([url])
    url_state_map = {url:QUEUED}
    print 'URL : ' + url
    try:
        content = get(url)
        found_urls = find_urls(url, content)
    except Exception, e:
        url_state_map[url] = e
        print 'Exception: %s' % e
    except KeyboardInterrupt, e:
        print url_state_map
        return
    else:
        for found_url in found_urls:
            if not url_state_map.get(found_url, NEW):
                if found_url.startswith('https://www.ptt.cc/bbs/Beauty/'):
                    url_queue.append(found_url)
                    url_state_map[found_url] = QUEUED
        url_state_map[url] = VISITED

    while url_queue:
        url = url_queue.popleft()
        content = get(url)
        for img_address in find_url_image(url, content):
            saveImage(img_address)


NEW = 0
QUEUED = 1
VISITED = 2

def search_urls(url):
    url_queue=deque([url])
    url_state_map = {url:QUEUED}
    while url_queue:
        url = url_queue.popleft()
        print url
        try:
            found_urls = find_urls(get(url))
        except Exception, e:
            url_state_map[url] = e
            print 'Exception: %s' % e
        except KeyboardInterrupt, e:
            print url_state_map
            return
        else:
            for found_url in found_urls:
                if not url_state_map.get(found_url, NEW):
                    url_queue.append(found_url)
                    url_state_map[found_url] = QUEUED
            url_state_map[url] = VISITED


if __name__ == '__main__':
    url = 'https://www.ptt.cc/bbs/Beauty/'
    if len(sys.argv) < 2:
        print 'Please input page number ( 1 ~ 500 )'
    else:
        for i in xrange(int(sys.argv[1])+1):
            current_page_url = urlparse.urljoin( url, 'index' + str(i+900) + '.html')
            print 'Current Url is :' + current_page_url
            search_Beauty(current_page_url);
            print 'Finish'
