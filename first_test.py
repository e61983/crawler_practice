#!/usr/bin/env python
# encoding: utf-8

import requests

url = 'http://download.post.gov.tw/post/download/MailBox_All.csv'

print requests.get(url).content
