#!/usr/bin/env python3
import requests
import sys
import time
import os
import getpass
import platform

if len(sys.argv) < 3:
    print('Usage: ./scraper.py <link to thread> <foldername>')
    print('Foldername will then be found within <foldername> in your home directory')
    sys.exit(1)
# Gets board and thread id from link and sets destination of files:
link = sys.argv[1]
board = link.split('/')[3]    # 'tv', 'wg', or similar
thread_id = link.split('/')[5]    # '114804039' or similar
url = 'https://a.4cdn.org/' + board + '/thread/' + thread_id + '.json'
content_url = 'https://i.4cdn.org/' + board + '/'

# Set destination folder:
system = platform.system()
if system == 'Linux':
    home = os.environ['HOME']
elif system == 'Windows':
    home == os.environ['HOMEPATH']
else:
    print('Unsupported system, exiting')
    sys.exit(2)

destination = f'{home}/{sys.argv[2]}'

# Create the destination folder
try:
    os.makedirs(destination, exist_ok=True)
except Exception as e:
    print(f'Could not create destination folder: {e}')
    sys.exit(3)

# Attempts to get the json-data for the thread:
resp = requests.get(url)
try:
    resp.raise_for_status()
except Exception as exc:
    print('Threw exception: %s' % exc)
    sys.exit(4)

# Parse posts and create list of filenames (composite of unix timestamp and file-extension)
posts = resp.json()
images = []
for post in posts['posts']:
    if post.get('filename'):
        # imagename is timestamp + file extension
        image = ''.join([str(post['tim']), post['ext']])
        images.append(image)

print('Starting download at: %s, it will take approx %s seconds' %
      (time.ctime(), len(images)))

# Parse the images list and download each with 1 second wait time (4chan API rules)
for image in images:
    imageurl = content_url + image
    target = destination + '/' + image

    print('\tDownloading: %s' % imageurl)
    try:
        r = requests.get(imageurl, stream=True)
        downloaded_file = open(target, 'wb')
        for chunk in r.iter_content(chunk_size=256):
            if chunk:
                downloaded_file.write(chunk)
    except requests.exceptions.RequestException as e:
        print('Could not download file, error: ', e)

    time.sleep(1)

print('Download complete at: %s' % time.ctime())
