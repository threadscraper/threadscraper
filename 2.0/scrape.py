#!/usr/bin/env python3
import requests
import time

def scraper(posts: list,
           start_time: int,
           content_url: str,
           destination: str,
           quiet: bool,
           verbose: bool,
           ) -> int:
    # Create list of images from start_time
    images = []
    if verbose:
        print(f'--> creating list of images to download')
    for post in posts:
        if post.get('filename'):
            # imagename is timestamp + file extension
            if post['time'] >= int(start_time):
                image = ''.join([str(post['tim']), post['ext']])
                images.append(image)

    if verbose:
        print(f'--> number of images to download: {len(images)}')

    # If there are images to download:
    if images:
        if not quiet:
            print(f'Starting download at: {time.ctime()}, it will take approx {len(images)} seconds')

        if verbose:
            print('--> downloading images with 1 second wait time')

        for image in images:
            imageurl = content_url + image
            target = destination + '/' + image

            if not quiet:
                print(f'\tDownloading: {imageurl}')
            try:
                r = requests.get(imageurl, stream=True)
                downloaded_file = open(target, 'wb')
                for chunk in r.iter_content(chunk_size=256):
                    if chunk:
                        downloaded_file.write(chunk)
            except requests.exceptions.RequestException as e:
                if not quiet:
                    print(f'Could not download file, error: {e}')

            time.sleep(1)

    # Return timestamp of last post
    return posts[-1]['time']
