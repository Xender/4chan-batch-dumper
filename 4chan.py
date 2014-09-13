#!/usr/bin/env python3

import sys
import json
import requests
import re

def scrape(image_urls_out_f, thread_info_out_f, thread_url):
	m = re.search(r'4chan.org/(.*?)/thread/(\d*)(:?/.*)?', thread_url)
	if not m:
		print("[FAIL] Invalid thread url, skipping: "+thread_url, file=sys.stderr)
		return

	board, thread_id = m.group(1, 2)

	r = requests.get(thread_url+'.json')
	r = requests.get('https://a.4cdn.org/{board}/thread/{thread_id}.json'.format(**locals()))

	if r.status_code == 404:
		print("[FAIL] Thread 404'd, skipping: "+thread_url, file=sys.stderr)
		return

	r.raise_for_status() # Throw at other errors.
	print("[ OK ] "+thread_url, file=sys.stderr)

	data = r.json()

	json.dump(data, thread_info_out_f,
		sort_keys=True,
		ensure_ascii=False,
		indent='\t')
	thread_info_out_f.write('\n')
	#TODO make whole file valid JSON.

	for post in data['posts']:
		try:
			filename = str(post['tim']) + post['ext']
		except KeyError:
			continue
		file_url = "http://images.4chan.org/{board}/src/{filename}".format(**locals())
		print(file_url, file=image_urls_out_f)
	image_urls_out_f.write('\n')

def main(args):
	image_urls_out_filename, thread_info_out_filename, *urls = args

	if not urls:
		urls = [ line.strip() for line in sys.stdin if not line.isspace() ]

	with open(image_urls_out_filename, 'w') as image_urls_out_f, open(thread_info_out_filename, 'w') as thread_info_out_f:
		for thread_url in urls:
			scrape(image_urls_out_f, thread_info_out_f, thread_url)

if __name__ == "__main__":
	main(sys.argv[1:])
