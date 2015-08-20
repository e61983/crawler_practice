#!/usr/bin/env python
# encoding: utf-8

import requests
import csv
import uniout
from os.path import basename
from os.path import exists
from pprint import pprint

url = 'http://download.post.gov.tw/post/download/MailBox_All.csv'
save_path = 'mailbox_location.csv'

def save(url, path = None):
    if not path:
        path = basename(url)
    with open(path, 'w') as f:
        f.write(requests.get(url).content)

def parse_to_mailbox_list(path):
    mailbox_list = []
    with open(save_path)  as f:
        mailbox_list = [address for address in csv.DictReader(f)]
    return mailbox_list

if not exists(save_path):
    save(url, save_path)

pprint(parse_to_mailbox_list(save_path))


# with open(save_path,'w') as f:
#   for line in f:
#       print line
