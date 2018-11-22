#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:post_process
   Author:jasonhaven
   date:18-11-22
-------------------------------------------------
   Change Activity:18-11-22:
-------------------------------------------------
"""
import json


def get_author_with_organization(data):
	result = []
	records = data[fname[:-5]]
	for record in records:  # 关键词下的论文集合
		for r in record:  # 论文下的作者集合
			author, organs = r[0], r[1]
			result.extend([(author, organ) for organ in organs if organ != 'None'])
	[print(rst) for rst in result]


def get_author_with_coauthor(data):
	result = []
	records = data[fname[:-5]]
	for record in records:  # 论文集和
		coauthors = set()
		for r in record:  # 每个论文下的作者集合
			coauthors.add(r[0])
		result.append(coauthors)
	[print(rst) for rst in result]


if __name__ == '__main__':
	# Reading data back
	input_dir = 'data/'
	fname = 'Deep Learning.json'
	with open(input_dir + fname, 'r') as f:
		data = json.load(f)
	print("\nauthor-organ\n")
	get_author_with_organization(data)
	print("\ncoauthors\n")
	get_author_with_coauthor(data)
