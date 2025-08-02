
import requests
import json
import os

# You can set environment variable PROXY_URL, or pass proxies dict to fetch functions
proxies = {}
proxy_env = os.getenv('PROXY_URL')
if proxy_env:
    proxies = {
        'http': proxy_env,
        'https': proxy_env
    }

def fetch_url(url):
    try:
        return requests.get(url, timeout=10, proxies=proxies)
    except Exception as e:
        print(f"Fetch error for {url}: {e}")
        return None

def fetch_ufcstats(event_url):
    res = fetch_url(event_url)
    if res and res.status_code == 200:
        # parse logic here...
        return []
    # fallback
    path = os.path.join(os.path.dirname(__file__), 'fallback_events.json')
    with open(path) as f:
        data = json.load(f)
    return data.get('fights', [])

# similar for tapology and sherdog using fetch_url
def fetch_tapology(event_slug):
    url = f"https://www.tapology.com/fightcenter/events/{event_slug}"
    res = fetch_url(url)
    if res and res.status_code == 200:
        return []
    return []

def fetch_sherdog(event_id):
    url = f"https://www.sherdog.com/events/{event_id}"
    res = fetch_url(url)
    if res and res.status_code == 200:
        return []
    return []

def fetch_all_sources(ufcstats_url, tapology_slug, sherdog_id):
    data = {
        'ufcstats': fetch_ufcstats(ufcstats_url),
        'tapology': fetch_tapology(tapology_slug),
        'sherdog': fetch_sherdog(sherdog_id)
    }
    combined = []
    for src in data.values():
        combined.extend(src or [])
    return combined
