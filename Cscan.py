# -*- coding: utf-8 -*-

import os
import time
from pyfiglet import Figlet
from optparse import OptionParser
import re
import requests
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning

lock = threading.Lock()
logging.captureWarnings(True)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check(url,timeout=1):
	name = url
	header = {
		'Host': 'www.baidu.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
	}
	try:
		r = requests.get(url, headers=header, verify=False, allow_redirects=True, timeout=timeout)
		code = r.status_code
	except Exception as error:
		code = "无法访问"

	with lock:
		code1 = str(code)
		if code1 != "无法访问":
			try:
				urllib3.disable_warnings()
				r = requests.get(url, headers=header, verify=False, allow_redirects=True, timeout=timeout)
				r.encoding = r.apparent_encoding
				title = re.findall("(?<=\<title\>)(?:.|\n)+?(?=\<)", r.text, re.IGNORECASE)[0].strip()
				print(title)
			except:
				title = "[ ]"
				print(title)

		else:
			title = " "
			print(title)

if __name__ == '__main__':
	# os.system('@echo off')
	os.system('chcp 936 >nul')
	f=Figlet(font='slant')
	print('\033[31m====================================================\033[0m')
	print('\033[34m{}\033[0m'.format(f.renderText('Scanner')))
	print('   \033[33mAuthor:LuckyRiver  ver:1.1  time:2022-09-08\033[0m')
	print('\033[31m====================================================\033[0m'+'\n')
	usage="\n"+"python3 %prog -u url"+"\n"+"python3 %prog -u url -t num"+"\n"+"python3 %prog -f url.txt"+"\n"+"python3 %prog -f url.txt -t"
	parser=OptionParser(usage=usage)
	parser.add_option('-u','--url',dest='url',help="target url")
	parser.add_option('-f','--file',dest='file',help="url file")
	parser.add_option('-t','--thread',type="int",dest='threads',help="thread number")
	(options,args)=parser.parse_args()
	start = time.time()

	if options.file:
		f=open(options.file,'r', encoding='utf-8')
		urls=f.readlines()
		thread_num = options.threads
		with ThreadPoolExecutor(max_workers=thread_num) as executor:
			for url in urls:
				if "http" in url:
					url=url.strip('\n')
				# print(url)
					check(url)
				else:
					url = "http://" + url.strip('\n')
					# print(url)
					check(url)
		print('\033[34m[#]扫描已完成\033[0m')
	end = time.time()
	print("总耗时:", end - start, "秒")


	if options.url:
		if "http" in options.url:
			check(options.url)
		else:
			httpurl = "http://" + options.url
			check(httpurl)
		print('\033[34m[#]扫描已完成\033[0m')
