import requests
from bs4 import BeautifulSoup

def fetch_event_data(event_url=None):
    base_url = 'https://ufcstats.com'
    if not event_url:
        upcoming_url = f'{base_url}/statistics/events/upcoming'
        try:
            res = requests.get(upcoming_url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            link = soup.select_one('.b-statistics__table-content a')
            event_url = link['href'] if link else None
        except Exception as e:
            return {'event_name':'Connection Error', 'date':'', 'location':'','fights':[],'error':str(e)}
    if not event_url:
        return {'event_name':'No Event URL', 'date':'', 'location':'','fights':[]}
    try:
        res2 = requests.get(event_url, timeout=10)
        res2.raise_for_status()
    except Exception as e:
        return {'event_name':'Connection Error','date':'','location':'','fights':[],'error':str(e)}
    soup2 = BeautifulSoup(res2.text, 'html.parser')
    event_name = soup2.select_one('.b-content__title-highlight').get_text(strip=True)
    details = soup2.select('.b-list__info-box')
    date, location = '', ''
    for box in details:
        text = box.get_text(strip=True)
        if 'Date' in text: date = text.replace('Date:','').strip()
        if 'Location' in text: location = text.replace('Location:','').strip()
    fights = []
    tables = soup2.select('table.b-fight-details__table')
    for table in tables:
        rows = table.select('tr')[1:]
        for r in rows:
            cols = r.select('td')
            if len(cols) >= 7:
                fights.append({
                    'fighter1': cols[1].get_text(strip=True),
                    'fighter2': cols[2].get_text(strip=True),
                    'stats_url1': cols[1].select_one('a')['href'],
                    'stats_url2': cols[2].select_one('a')['href']
                })
    return {'event_name':event_name, 'date':date, 'location':location, 'fights':fights}
