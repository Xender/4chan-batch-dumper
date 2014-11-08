Yet another 4chan thread dumper.
Commandline, batch style.
In Python 3.

Usage
=====

Stdin mode:
-----------

	./4chan.py < threads.txt

threads.txt:

	<url1>
	<url2>
	...

Commandline mode:
-----------------

	./4chan.py <url1> [<url2>...]

Output
======

Files (saved in current directory):
- `thread.{board}.{thread_id}.{thread_name}.json` for each thread.
- All images from a thread.

Supports incremental mode - already existing image files are not overwritten.

Known issues
============

- TODO: file transactions - now interrupting the program can leave partially written thread JOSN files and maybe images.
Partially written image filess are more of a deal, as they won't be redownloaded when script is run next time.
