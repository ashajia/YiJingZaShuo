#!/usr/bin/python3
import requests
from lxml import etree
import os, re, json

index_url = 'http://www.quanxue.cn/CT_NanHuaiJin/YiJingIndex.html'
base_url = 'http://www.quanxue.cn/CT_NanHuaiJin'
headers = {
		'User-Agent': 
		'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36  \
		(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
		}

def get_index(url):
	# 获取目录页内容
	rps = requests.get(url, headers = headers)
	rps.encoding = 'utf-8'
	return rps.text

class ParserIndex:
	def __init__(self, text):
		self.html = etree.HTML(text, etree.HTMLParser())
		# 获取一级标题内容
		self.title_1 = self.html.xpath('//div[@class="indextdintr n1"]/text()')

	def parser_title(self):
		self.index_dict = {}
		# enumerate 遍历列表的下标和值
		for idx, val in enumerate(self.title_1):
			position = str(idx + 1)
			path_a = '//div[@class="indextable n2"][' + position + ']//li/a/'
			# 输出 text和href两个列表，通过dict(zip(将两个列表zip成一个字典
			#title_2_text = '{}、{}'.format(position, self.html.xpath(path_a + '/text()'))
			title_2_text = self.html.xpath(path_a + '/text()')
			title_2_href = self.html.xpath(path_a + '/@href')
			title_2 = dict(zip(title_2_text, title_2_href))
			self.index_dict[val] = title_2
		return self.index_dict


def get_url(index):
	# 参数为目录字典
	content_name_url = {}
	chapter = 0
	for header_1,title_url in index.items():
		for title,url in title_url.items():
			chapter += 1
			file_name = '{}/{}、{}.md'.format(header_1,chapter, title)
			full_url = '{}/{}'.format(base_url, url)
			content_name_url[file_name] = full_url

	return content_name_url



if __name__ == '__main__':
	index_text = get_index(index_url)
	p = ParserIndex(index_text)
	index = p.parser_title()
	print(json.dumps(get_url(index),sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False))
