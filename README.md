# threadscraper
Python script to scrape images from a 4chan thread and save them to a folder in your home folder. Should work on both Windows and Linux-based systems.

### Features:
- Scrape a thread in a one-off type fashion
- Watch a thread to continuously download all images with a five minute wait time between scrapes.
- Set your own wait-time interval if 5 minutes is too long to wait

### Usage:
`pip install -r requirements.txt`

`python3 threadscraper.py --help`

##### Examples:
Get in depth information about the scripts behavour:
`python3 threadscraper -v some_url some_folder`

Watch a thread:
`python3 threadscraper -w some_url some_folder`

Watch a thread with a different wait-time interval:
`python3 threadscraper -w -i 120 some_url some_folder`

Run the script in quiet mode:
`python3 threadscraper -q some_url some_folder`

### Contact:
Feel free to open an issue if there are any questions
