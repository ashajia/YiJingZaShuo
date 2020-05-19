#!/usr/bin/python3

import requests
from lxml import etree
import re

content_url = 'http://www.quanxue.cn/CT_NanHuaiJin/YiJing/YiJing81.html'
base_url = 'http://www.quanxue.cn/CT_NanHuaiJin/YiJing/'
headers = {
                'User-Agent': 
                'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36  \
                (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                }

def get_content_html(url):
	c_resp = requests.get(url, headers = headers)
	c_resp.encoding = 'utf-8'
	return c_resp.text

def get_content_text(text):
	# 返回p标签内容 和span标签内容
	html = etree.HTML(text, etree.HTMLParser())
	content_p = html.xpath('//p')
#	content_span = html.xpath('//span[@class="qiangdiao1"]')
	content_span = html.xpath('//span[contains(@class,"qiangdiao")]')
	new_content_span = []
	return (content_p, content_span)

def format_content(content_p_list, content_span_list):
	# 返回p标签内容，其中span标签被替换为自定义内容
	content_text_list = []
	for content in content_p_list:
		content_text = []
		content_p_string = content.xpath('string(.)')
		content_p_string = content_p_string.replace('\n','').replace('\r','')
		for span in content_span_list:
			if span.text is None:
				if span.find('img') is not None:
					img_url = base_url + span.find('img').attrib['src']
					md_img = '![bagua](https://cors.zme.ink/{})'.format(img_url)
					content_p_string = content_p_string.replace('“”','“'+md_img+'”')
				elif span.find('big') is not None:
					big_text = span.find('big').text
					content_p_string = content_p_string.replace('“'+big_text+'”', '“<font size=4>``'+ big_text +'``</font>”')
			else:
				f_span = '``{}``'.format(span.text)
				content_p_string = re.sub(r'“'+span.text+'”', '“'+f_span+'”',content_p_string)
		content_text.append('&emsp;' + content_p_string + '\n___\n')
		content_text_list.append(content_text)
	return content_text_list

def create_md(file_name, content_list):
	with open(file_name, 'a') as f:
		for c_list in content_list:
			for c in c_list:
				f.write(c)
		f.write('[返回目录](../../master/README.md#目录)')
		print('  - Create {} Success'.format(file_name))

if __name__ == '__main__':
	content_text = get_content_html(content_url)
	content_tag_list = get_content_text(content_text)
	content_list = format_content(*content_tag_list)
	create_md('测试', content_list)
