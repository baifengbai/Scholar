#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:main
   Author:jasonhaven
   date:2018/4/17
-------------------------------------------------
   Change Activity:2018/4/17:
-------------------------------------------------
"""

import log
from urllib import request
from bs4 import BeautifulSoup
import random
import time

logger = log.Logger().get_logger()

headers = {
	'Referer': 'http://xueshu.baidu.com/',
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

retry=3
delay=1

def download_html(url):
	'''
	下载网页

	:param url:
	:param retry:
	:return:
	'''
	global retry
	global delay
	try:
		proxy_list=[p.strip() for p in open('ProxyGetter/proxies.txt').readlines()]
		proxy=random.choice(proxy_list)
		proxy_handler = request.ProxyHandler({'http': proxy})
		opener=request.build_opener(proxy_handler)
		request.install_opener(opener)
		logger.info('proxy = {}'.format(proxy))

		req = request.Request(url=url, headers=headers)
		resp = request.urlopen(req, timeout=5)
		
		# resp=opener.open(url)
		if resp.status != 200:
			logger.error('url open error. url = {}'.format(url))
		html_doc = resp.read()
		return html_doc
	except Exception as e:
			logger.error("failed and retry to download url {} delay = {}".format(url, delay))
			if retry > 0:
				time.sleep(delay)
				retry -= 1
				return download_html(url)

print(download_html('https://mp.weixin.qq.com/s/83oOI0oJ_QN-o1LZ439UVQ'))