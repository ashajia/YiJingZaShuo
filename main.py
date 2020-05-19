#!/usr/bin/python3
import book_change as bc
import content as ct
import os

root_path = '.'
index_url = 'http://www.quanxue.cn/CT_NanHuaiJin/YiJingIndex.html'
base_url = 'http://www.quanxue.cn/CT_NanHuaiJin'
headers = {
                'User-Agent': 
                'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36  \
                (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                }

index_text = bc.get_index(index_url)
p = bc.ParserIndex(index_text)
index = p.parser_title()
#print(type(bc.get_url(index)))

for filename, content_url in bc.get_url(index).items():
	index_path = os.path.join(root_path, os.path.dirname(filename))
	if os.path.exists(index_path):
		pass
	else:
		os.mkdir(index_path)
		print('Create Path {}'.format(index_path))
	full_filename = os.path.join(root_path, filename)

	print('  + Start Create {}'.format(filename))
	content_text = ct.get_content_html(content_url)
	content_tag_list = ct.get_content_text(content_text)
	content_list = ct.format_content(*content_tag_list)
	ct.create_md(full_filename, content_list)
	#print(str(content_list))
