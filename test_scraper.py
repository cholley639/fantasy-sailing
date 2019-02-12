import requests
from bs4 import BeautifulSoup


def get_html_from_url(url):
    res = requests.get(url)
    return res.text


print(get_html_from_url('https://scores.collegesailing.org/s19/harris-kempner/sailors/'))
print('done')
