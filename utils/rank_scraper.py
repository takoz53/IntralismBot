import re, requests
from bs4 import BeautifulSoup
from utils.extensions import threaded

def cleanString(html):
    """Cleans String from unnecessary things"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)

def scrapeTop(call_back=None):
    """Scrapes Top10 Data from Website"""
    top_url = "https://intralism.khb-soft.ru/?page=ranks"
    source = BeautifulSoup(requests.get(top_url, headers={'User-Agent': 'IntraBot'}).content, 'html.parser')
    
    result = [item for item in source.find_all('tr', class_='clickable-row bgimg', limit=10)]
    data_list = []

    for item in result:
        array = item.find_all('td')
        if len(array) < 6: continue
        rank = array[0]
        pic = array[1]
        country = array[2]
        point = array[3]
        accuracy = array[4]
        misses = array[5]
        
        data = {
            'rank': rank.text.strip(),
            'imagePath': pic.find('img')['src'],
            'name': pic.text.strip(),
            'country': country.text.strip(),
            'point': point.text.strip(),
            'accuracy': accuracy.text.strip(),
            'misses': misses.text.strip()
        }

        data_list.append(data)
    
    if callable(call_back):
        call_back(data_list)

    return data_list
    
def scrape(steam_id):
    """Scrapes userdata from given Steam ID"""
    url = 'https://intralism.khb-soft.ru/?player=' + str(steam_id)
    source = BeautifulSoup(requests.get(url, headers={'User-Agent': 'IntraBot'}).content, 'html.parser')

    name = cleanString(str(source.find('div', class_ = 'mt-5').h1)).split('#')[0]
    avatar = source.find('img', class_='float-left avatar')['src']
    div = source.find('div', class_ = 'col-md-4 text-md-right')
    stats = cleanString(str(div)).split('\n')
    stats_list = []
    
    for line in stats:
        stats_list.append(line)
    
    stats_list = list(filter(None, stats_list)) # clean empty entries
    del stats_list[-1] # clean social

    stats_list.append(name)
    stats_list.append(avatar)
    return stats_list
