#!/usr/bin/env python3

import sys
import json
import requests
import re

def scrape(thread_url):
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

	with open('thread.{board}.{thread_id}.json'.format(**locals()), 'w') as thread_f:
		json.dump(data, thread_f,
			sort_keys=True,
			ensure_ascii=False,
			indent='\t')
		thread_f.write('\n')

	for post in data['posts']:
		try:
			filename = str(post['tim']) + post['ext']
		except KeyError: # No image in post
			continue
		file_url = "http://images.4chan.org/{board}/src/{filename}".format(**locals())
		print(file_url)
	sys.stdout.write('\n')

def main(urls):
	if not urls:
		urls = [ line.strip() for line in sys.stdin if not line.isspace() ]

	for thread_url in urls:
		scrape(thread_url)

if __name__ == "__main__":
	main(sys.argv[1:])
