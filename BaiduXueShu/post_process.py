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
import os


def get_author_with_organization(data):
	result = set()
	records = list(data.values())[0]
	for i, record in enumerate(records):  # 关键词下的论文集合
		for r in record:  # 论文下的作者集合
			author, organs = r[0], r[1]
			for organ in organs:
				if organ != 'None':  # 不为空的情况下
					# if organ.find(',')!=-1:#不止一个机构组织(会产生误判)
					# 	for org in organ.split(','):
					# 		result.add((author, org))
					# else:
					# 	result.add((author, organ))
					result.add((author, organ))
	# for rst in result:
	# 	print(rst)
	return result


def get_author_with_coauthor(data):
	result = set()
	records = list(data.values())[0]
	for i, record in enumerate(records):  # 关键词下的论文集合
		coauthors = set()
		for r in record:  # 每个论文下的作者集合
			if r[0] != 'None':
				coauthors.add(r[0])
		if coauthors != set():
			coauthors=list(coauthors)
			if len(coauthors)>1:
				for i in range(len(coauthors)):
					for j in range(i+1,len(coauthors)):
						result.add('{}\t{}'.format(coauthors[i],coauthors[j]))
			else:
				result.add('\t'.join(coauthors))

	# for rst in result:
	# 	print(rst)	

	return result


def get_from_dir(dir):
	if os.path.exists("author_organ.csv"):
		os.remove("author_organ.csv")
	if os.path.exists("author_coauthor.csv"):
		os.remove("author_coauthor.csv")
	fp1 = open('author_organ.csv', 'a', encoding='utf-8')
	fp2 = open('author_coauthor.csv', 'a', encoding='utf-8')
	for dirpath, dirnames, filenames in os.walk(dir):
		for fname in filenames:
			fpath = dirpath + os.path.sep + fname
			if os.path.getsize(fpath)==0:
				continue
			try:
				with open(fpath, 'r', encoding='utf-8') as f:
					data = json.load(f)
					author_organ = get_author_with_organization(data)
					for (a, b) in author_organ:
						fp1.write("{}\t{}\n".format(a, b))

					author_coauthor = get_author_with_coauthor(data)
					for sent in author_coauthor:
						fp2.write(sent + '\n')
			except Exception as e:
				print("Error in load file = {}".format(fpath))
				continue
	fp1.close()
	fp2.close()


if __name__ == '__main__':
	input_dir = 'data/'
	get_from_dir(input_dir)
