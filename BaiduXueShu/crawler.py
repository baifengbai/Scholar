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
import json
import codecs
import time
import datetime
from urllib import parse
from urllib import request
from bs4 import BeautifulSoup
import string

logger = log.Logger().get_logger()

headers = {
	'Host': 'xueshu.baidu.com',
	'Referer': 'http://xueshu.baidu.com/',
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

re_try = 3
base_url = "https://xueshu.baidu.com/s?"


class Crawler():
	def download_html(self, url, retry):
		'''
		下载网页

		:param url:
		:param retry:
		:return:
		'''
		try:
			req = request.Request(url=url, headers=headers)
			resp = request.urlopen(req, timeout=5)
			if resp.status != 200:
				logger.error('url open error. url = {}'.format(url))
			html_doc = resp.read()
			return html_doc
		except Exception as e:
			logger.error("failed and retry to download url {} delay = 2".format(url))
			if retry > 0:
				time.sleep(2)
				return self.download_html(url, retry - 1)

	def extract_full_organization(self, query):
		'''
		抽取机构名字

		:param query:
		:return:
		'''
		# wd=author%3A%28Yann%20LeCun%29&tn=SE_baiduxueshu_c1gjeupa&sc_hit=1&bcp=2&ie=utf-8&tag_filter=%20%20%20affs%3A%28New%20York%20University%29
		name = "None"
		query_dict = parse.parse_qs(query)
		if query_dict == {}: return "None"
		organ = query_dict['tag_filter'][0]
		# ['   affs:(New York University)']
		name = organ[organ.index("affs:") + len("affs:"):]
		return name

	def extract_organizations(self, author):
		'''
		抽取机构信息

		:param author:
		:return:
		'''
		organizations = []
		logger.info("extract information for author = {}".format(author))

		# 构造请求
		# https://xueshu.baidu.com/s?wd=author%3A%28Yann%20LeCun%29%20
		query = {}
		query['wd'] = parse.quote("author:" + author, safe=string.printable)
		query = parse.urlencode(query)

		# 构造地址
		url = base_url + query

		html_doc = self.download_html(url, re_try)
		soup = BeautifulSoup(html_doc, "lxml")

		try:
			# 获取左侧栏
			leftnav_div = soup.find("div", id="leftnav")
			leftnav_items = leftnav_div.find_all('div', class_="leftnav_item")

			# 抽取机构
			organs_block = leftnav_items[-1].find("div", class_="leftnav_list_cont").find_all('a')
			for organ in organs_block:
				organ_full_name = self.extract_full_organization(organ.get('href')[3:])
				organizations.append(organ_full_name)
		except Exception as e:
			logger.error("extract organization for {} url = {}".format(author, url))
		return organizations

	def extract_html_doc(self, html_doc):
		'''
		抽取网页

		:param html_doc:
		:return:
		'''
		records = []

		soup = BeautifulSoup(html_doc, "lxml")
		result_div = soup.find('div', id="bdxs_result_lists")
		result_lists = result_div.find_all("div", class_="result sc_default_result xpath-log")

		for i, result in enumerate(result_lists):
			record = []

			logger.info("extract for item = {}  delay = 2".format(i))
			time.sleep(2)

			# 抽取论文题目paper_title和超链接total_href
			h3 = result.find("h3")
			paper_title = h3.get_text().strip()
			sub_href = h3.find('a').get('href')
			total_href = "http://xueshu.baidu.com" + sub_href
			logger.info('title = {}, url = {}'.format(paper_title, total_href))

			# 抽取作者信息
			info = result.find('div', class_="sc_info")
			authors_block = info.find('span').find_all('a')
			authors_qs = [x.get('href').strip()[3:] for x in authors_block]

			for query in authors_qs:
				time.sleep(1.5)
				# 对query做一个预处理，截取部分留下
				# /s?wd=author%3A%28Yann%20LeCun%29%20&tn=SE_baiduxueshu_c1gjeupa
				# /s?wd=author%3A%28Yi%20Sun%29%20Dept.%20of%20Inf.%20Eng.%2C%20Chinese%20Univ.%20of%20Hong%20Kong%2C%20Hong%20Kong%2C%20China
				query = query[:query.index("%29%20") + len(("%29%20"))]
				query_dict = parse.parse_qs(query)
				author = query_dict['wd'][0][7:]
				# 作者的机构
				organizations = self.extract_organizations(author)
				# 添加记录
				record.append((author, organizations))
				records.append(record)
		return records

	def begin(self, start_page=0, end_page=1):
		'''
		开始抓取

		:param keywords:
		:param start_page:
		:param end_page:
		:return:
		'''

		keywords = crawler.load_keywords()[:2]

		for i, key in enumerate(["Deep Learning", "Computer Science"]):
			logger.info("search keyword = {} {}/{} delay = 2".format(key, i + 1, len(keywords)))
			time.sleep(2)
			# https://xueshu.baidu.com/s?wd=Deep+Learning&tn=SE_baiduxueshu_c1gjeupa&cl=3&ie=utf-8&bs=Deep+Learning&f=8&rsv_bp=1&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D

			# 分页查询
			for page in range(start_page, end_page + 1):
				logger.info("extract page = {} delay = 2".format(page))
				time.sleep(2)

				# 构造请求
				query = {}
				pn = page * 10
				query['wd'] = parse.quote(key, safe=string.printable)
				query['pn'] = str(pn)
				query = parse.urlencode(query)

				# 构造地址
				url = base_url + query

				html_doc = self.download_html(url, re_try)

				records = self.extract_html_doc(html_doc)

				logger.info("done with keyword = {} at page = {}".format(key, page))

			self.save(key, records, True)

			logger.info("done with keyword = {} {}/{} ".format(key, i, len(keywords)))

	def save(self, keyword, records, append_mode):
		fmode = "a" if append_mode else "w"
		fname = "{}.json".format(keyword)
		fpath = "data/{}".format(fname)
		if records == []: return
		with codecs.open(fpath, fmode, encoding='utf-8') as f:
			json.dump({keyword: records}, f)

	def load_keywords(self, fpath="english.csv"):
		'''
		加载关键词词表

		:return: 过滤之后的词表 [计算机技术,计算机技术,计算机技术]
		'''
		with codecs.open(fpath, 'r', encoding='utf-8') as f:
			keywords = list(set(key.strip() for key in f.readlines()))
			return keywords


if __name__ == '__main__':
	begin = datetime.datetime.now()

	crawler = Crawler()
	crawler.begin(start_page=0, end_page=0)  # 时间估计：2个关键字，5页（一页10条），约13min

	end = datetime.datetime.now()
	logger.info('finished in {}s'.format(end - begin))
