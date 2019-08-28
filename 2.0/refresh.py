import requests

def refresh_post_list(url: str, quiet: bool, verbose: bool) -> list:
    resp = requests.get(url)
    posts = []
    try:
        resp.raise_for_status()
        posts = resp.json()['posts']
    except Exception as exc:
        raise

    return posts
