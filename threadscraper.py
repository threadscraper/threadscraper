#!/usr/bin/env python3
import argparse
from datetime import datetime, timedelta
import os
import platform
import sys
import time

from scrape import scraper
from refresh import refresh_post_list


def main():
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('url', help='URL to the 4chan thread you want to scrape', type=str)
    parser.add_argument('destination', help='Destination folder in your home folder', type=str)

    # Optional arguments
    parser.add_argument('-q', '--quiet',
                        help='Run the script in quiet mode, no outputs',
                        action='store_true',
                        default=False)
    parser.add_argument('-v', '--verbose',
                        help='Run with increased verbosity',
                        action='store_true',
                        default=False)
    parser.add_argument('-w', '--watch',
                        help='Watch the thread, will check thread every 5 minutes for new posts until thread 404s',
                        action='store_true',
                        default=False)
    parser.add_argument('-i', '--interval',
                        help='Specify the wait-time when watching a thread in seconds',
                        type=int)

    args = parser.parse_args()

    # Set behaviour:
    verbose = args.verbose
    quiet = args.quiet
    watch = args.watch
    interval = 300
    if args.interval:
        interval = args.interval

    # Set variables
    link = args.url
    destination = args.destination
    board = link.split('/')[3]    # 'tv', 'wg', or similar
    thread_id = link.split('/')[5]    # '114804039' or similar
    url = f'https://a.4cdn.org/{board}/thread/{thread_id}.json'
    content_url = f'https://i.4cdn.org/{board}/'

    # Determine platform/OS and set appropriate path
    system = platform.system()
    if system == 'Linux':
        home = os.environ['HOME']
        destination = f'{home}/{destination}'
    elif system == 'Windows':
        home == os.environ['HOMEPATH']
        destination = f'{home}\{destination}'
    else:
        if not quiet:
            print('Unsupported system, exiting')
        sys.exit(2)

    if verbose:
        print('Will scrape using the following information:')
        print(f'\tLink: \t\t{link}')
        print(f'\tBoard: \t\t{board}')
        print(f'\tThread ID: \t{thread_id}')
        print(f'\tURL: \t\t{url}')
        print(f'\tContent URL: \t{content_url}')
        print(
            f'\tDestination: \t{destination}\n')

    # Create the destination folder
    if verbose:
        print(f'--> creating folder: {destination}')
    try:
        os.makedirs(destination, exist_ok=True)
    except Exception as e:
        if not quiet:
            print(f'Could not create destination folder: {e}')
        sys.exit(3)

    # Get the thread in JSON-representation:
    try:
        if verbose:
            print(f'--> getting the thread metadata from thread id: {board}/{thread_id}')
        posts = refresh_post_list(url, quiet, verbose)
    except Exception as e:
        if not quiet:
            print(f'Could not get thread metadata, reason: {e}')
        sys.exit(4)

    # Set timestamp
    start_time = posts[0]['time']

    # Provide more verbose information about the thread:
    if verbose:
        first_post = posts[0]
        if first_post.get('sub'):
            title = first_post['sub']
        else:
            title = None
        no_of_images = first_post['images']
        no_of_replies = first_post['replies']
        time_of_first_post = datetime.utcfromtimestamp(
            start_time).strftime('%Y-%m-%d %H:%M:%S')

        print('--> metainformation about the thread:')
        if title:
            print(f'\tTitle: {title}')
        print(f'\tNumber of images: {no_of_images}')
        print(f'\tNumber of replies: {no_of_replies}')
        print(f'\tTime of first post: {time_of_first_post} UTC')

    new_time = scraper(posts, start_time, content_url,
                       destination, quiet, verbose)
    if verbose:
        print(f'--> timestamp of last post: {new_time}')

    if watch:
        if not quiet:
            print('--- watching thread ---')
        while True:
            if verbose:
                print(f'--> waiting {timedelta(seconds=interval)} before refreshing thread')
            time.sleep(interval)

            if verbose:
                print('--> refreshing list of posts')
            posts = refresh_post_list(url, quiet, verbose)

            # Check if thread is closed:
            if posts[0].get('closed'):
                if posts[0]['closed']:
                    if not quiet:
                        print('Thread is closed, exiting')
                    break
            if verbose:
                print('--> attempting to download new images')
            new_time = scraper(posts, new_time, content_url,
                               destination, quiet, verbose)

    print('All images are downloaded, goodbye.')


if __name__ == '__main__':
    main()
