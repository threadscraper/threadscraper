#!/usr/bin/env python3
import sys
import os
import argparse
import platform


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument('', help='', type=str)
    parser.add_argument('-q', '--quiet', help='Run the script in quiet mode, no outputs', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='Run with increased verbosity', action='store_true', default=False)
    parser.add_argument('-w', '--watch', help='Watch the thread, will check thread every 5 minutes for new posts until thread 404s', action='store_true', default=False)
    parser.add_argument('url', help='URL to the 4chan thread you want to scrape', type=str)
    parser.add_argument('destination', help='Destination folder in your home folder', type=str)

    args = parser.parse_args()

    if args.url is None:
        print('URL is missing, exiting')
        sys.exit(1)

    # Set behaviour:
    verbose = args.verbose
    quiet = args.quiet
    watch = args.watch

    # Set variables
    link = args.url
    destination = args.destination
    board = link.split('/')[3]    # 'tv', 'wg', or similar
    thread_id = link.split('/')[5]    # '114804039' or similar
    url = f'https://a.4cdn.org/{board}/thread/{thread_id}.json'
    content_url = f'https://i.4cdn.org/{board}/'


    # Determine platform/OS and set appropriate path
    if not destination:
        if not quiet:
            print('No destination folder given, exiting')
        sys.exit(2)
    else:
        system = platform.system()
        if system == 'Linux':
            home = os.environ['HOME']
        elif system == 'Windows':
            home == os.environ['HOMEPATH']
        else:
            if not quiet:
                print('Unsupported system, exiting')
            sys.exit(3)
        destination = f'{home}/{destination}'

    if verbose:
        print('Will scrape using the following information:')
        print(f'\tLink: {link}')
        print(f'\tBoard: {board}')
        print(f'\tThread ID: {thread_id}')
        print(f'\tURL: {url}')
        print(f'\tContent URL: {content_url}')
        print(f'\tYou will find the pictures in the following folder: {destination}\n')

    # Create the destination folder
    if verbose:
        print(f'--> creating folder: {destination}')
    try:
        os.makedirs(destination, exist_ok=True)
    except Exception as e:
        if not quiet:
            print(f'Could not create destination folder: {e}')
        sys.exit(4)

    # Get the thread in JSON-representation:
    if verbose:
        print(f'--> getting the thread metadata from thread id: {thread_id}')
    resp = requests.get(url)
    try:
        resp.raise_for_status()
    except Exception as exc:
        if not quiet:
            print(f'Could not get thread metadata, reason: {e}')
        sys.exit(5)

if __name__ == '__main__':
    main()
