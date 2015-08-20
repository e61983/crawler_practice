#!/usr/bin/env python
# encoding: utf-8

import requests

url = 'http://download.post.gov.tw/post/download/MailBox_All.csv'
save_path = 'mailbox_location.csv'

with open(save_path, 'w') as f:
    f.write(requests.get(url).content)

with open(save_path, 'r')  as f:
    print f.read()

# with open(save_path,'w') as f:
#   for line in f:
#       print line   
