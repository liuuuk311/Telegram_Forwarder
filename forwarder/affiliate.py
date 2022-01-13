import random

import requests
import re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

token = '961b2a0b2de7548fd8a6f58c86359849dafd374a'

API_URL_BITLINKS = "https://api-ssl.bitly.com/v4/bitlinks"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}


def get_short_url(long_url):
    long_url = long_url.strip()
    response = requests.post(
        url=API_URL_BITLINKS,
        json={"long_url": long_url},
        allow_redirects=False,
        timeout=2000,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_json = response.json()

    return response_json.get('link', long_url)


def prepare_url(link):
    if not link.startswith('https://') and not link.startswith('http://'):
        link = 'https://' + link

    return link


def overwrite_affiliate(url):
    try:
        res = requests.head(prepare_url(url), headers=headers, allow_redirects=True)
        url = res.url
    except requests.exceptions.ConnectionError:
        raise ValueError("Impossibile verificare il link completo. Errore di connessione")

    if 'amazon.it' in url:
        params = amazon_affiliate()
        extra = {"store": "amz"}
    elif 'banggood.com' in url:
        params = banggood_affiliate()
        extra = {"store": "bg"}
    elif 'drone24hours.com' in url:
        params = drone24_affiliate()
        extra = {
            "store": "d24",
            "code": "NorthFPV5",
            "desc": "Se siete nuovi utenti usando il coupon `drone10`, dovreste ottenere uno sconto. "
                    "I coupon non sono cumulabili"
        }
    elif 'personaldrones.it' in url:
        params = personaldrones_affiliate()
        extra = {"store": "pd"}
    else:
        raise ValueError("Non siamo affiliati a questo store")

    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.pop('rmmds', None)
    query.update(params)

    url_parts[4] = urlencode(query)

    url = urlunparse(url_parts)

    # return {"link": get_short_url(url), **extra}
    return get_short_url(url)


def banggood_affiliate():
    if random.random() < 0.75:
        return {'p': 'G6122253473537202010', 'utm_campaign': 'NorthFPV'}
    else:
        return {'p': 'YN241438687092016024'}


def amazon_affiliate():
    return {'ref': 'as_li_ss_tl', 'tag': 'iamlucafpv-21'}


def drone24_affiliate():
    return {'D24H': 'northfpvofficial'}


def personaldrones_affiliate():
    return {'id': '13907'}

