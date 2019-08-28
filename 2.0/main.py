#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument('', help='', type=str)
    parser.add_argument('-u', '--url', help='URL to the 4chan thread you want to scrape', type=str)
    parser.add_argument('-q', '--quiet', help='Run the script in quiet mode, no outputs', action='store_true')
    parser.add_argument('-v', '--verbose', help='Run with increased verbosity', action='store_true')
    parser.add_argument('-w', '--watch', help='Watch the thread, will check thread every 5 minutes for new posts until thread 404s', action='store_true')

    args = parser.parse_args()

    # Set behaviour:
    verbose = args.verbose
    quiet = args.quiet
    watch = args.watch

    # Set variables
    link = args.url
    board = link.split('/')[3]    # 'tv', 'wg', or similar
    thread_id = link.split('/')[5]    # '114804039' or similar
    url = f'https://a.4cdn.org/{board}/thread/{thread_id}.json'
    content_url = f'https://i.4cdn.org/{board}/'

    if verbose:
        print('Will scrape using the following information:')
        print(f'\tLink: {link}')
        print(f'\tBoard: {board}')
        print(f'\tThread ID: {thread_id}')
        print(f'\tURL: {url}')
        print(f'\tContent URL: {content_url}')

if __name__ == '__main__':
    main()
