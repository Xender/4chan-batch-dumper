#!/usr/bin/env python3

import json
import os.path
import re
import sys
import urllib.request

import requests


def scrape(thread_url):
	m = re.search(r'4chan.org/(.*?)/thread/(\d*)(:?/.*)?', thread_url)
	if not m:
		print("[FAIL] Invalid thread url, skipping: "+thread_url, file=sys.stderr)
		return None

	board, thread_id = m.group(1, 2)

	r = requests.get(thread_url+'.json')
	r = requests.get('https://a.4cdn.org/{board}/thread/{thread_id}.json'.format(**locals()))

	if r.status_code == 404:
		print("[FAIL] Thread 404'd, skipping: "+thread_url, file=sys.stderr)
		return None

	r.raise_for_status() # Throw at other errors.
	print("[ OK ] "+thread_url, file=sys.stderr)

	data = r.json()
	posts = data['posts']

	semantic_url = posts[0]['semantic_url']
	with open('thread.{board}.{thread_id}.{semantic_url}.json'.format(**locals()), 'w') as thread_f:
		json.dump(data, thread_f,
			sort_keys=True,
			ensure_ascii=False,
			indent='\t')
		thread_f.write('\n')

	return board, thread_id, posts

def download(url, filename):
	if not os.path.exists(filename):
		sys.stderr.write(filename+" ")
		sys.stderr.flush()
		urllib.request.urlretrieve(url, filename)
		sys.stderr.write("OK\n")

def process_thread(board, thread_id, posts):
	for post in posts:
		try:
			filename = str(post['tim']) + post['ext']
		except KeyError: # No image in post
			continue

		img_url = 'http://images.4chan.org/{board}/src/{filename}'.format(**locals())
		download(img_url, filename)

def main(urls):
	if not urls:
		urls = [ line.strip() for line in sys.stdin if not line.isspace() ]

	for thread_url in urls:
		thread = scrape(thread_url)
		if thread:
			process_thread(*thread)


if __name__ == "__main__":
	main(sys.argv[1:])
