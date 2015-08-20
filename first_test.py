#!/usr/bin/env python
# encoding: utf-8

import requests
import csv
import uniout
from os.path import basename
from os.path import exists

url = 'http://download.post.gov.tw/post/download/MailBox_All.csv'
save_path = 'mailbox_location.csv'

def save(url, path = None):
    if not path:
        path = basename(url)
    with open(path, 'w') as f:
        f.write(requests.get(url).content)

if not exists(save_path):
    save(url, save_path)

with open(save_path)  as f:
    for row in csv.reader(f):
        print row

# with open(save_path,'w') as f:
#   for line in f:
#       print line
