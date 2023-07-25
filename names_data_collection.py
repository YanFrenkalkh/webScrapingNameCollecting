import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# base URLS
base_url = 'https://en.wikipedia.org'
wiki_url = 'https://en.wikipedia.org/wiki/Category:Given_names'
surnames_url = 'https://en.wikipedia.org/wiki/Category:Surnames'

# Data sets
all_names = []
base_page_id = []
result_tuples = []


# Page pars function
def extract_names_from_url(url):
    # Get http request
    response = requests.get(url)

    # Check if the page whase succsesfuly opend
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Serch for the div that holds the namse and extruct the names ul
        given_names_text = soup.find('div', {'id': 'mw-pages'}).find('div', {'class': 'mw-category mw-category-columns'}).findAll('li')

        # Clean the data and stor in memory
        for given_name in tqdm(given_names_text):
            if given_name != '\n':
                all_names.append(given_name.get_text())

        # Extruct the next 'next page'
        next_page_text = soup.find('div', {'class': 'mw-category-generated'}).findAll('a')[-1].text

        if next_page_text == 'next page':
            # Extruct the next page partial url
            next_page_partial_url = soup.find('div', {'class': 'mw-category-generated'}).findAll('a')[-1]['href']
            # Concar the new next page url
            next_page_url = base_url + next_page_partial_url
            extract_names_from_url(next_page_url)


def make_data_set_tupple(page_title):
    def get_wikidata_info(page_id):
        # Get wikidata url
        url = f"https://www.wikidata.org/wiki/{page_id}"
        html = requests.get(url).content.decode('utf-8')

        # Parse the data
        soup = BeautifulSoup(html, 'html.parser')
        # Get description and rows
        description = soup.find('table').findAll('tr')[1].findAll('td')[1].text
        wiki_rows = soup.find('ul', {'class': 'wikibase-sitelinklistview-listview'}).findAll('li', {'class': 'wikibase-sitelinkview'})
        for row in tqdm(wiki_rows):
            # Get langude and entry
            langude = row.findAll('span', {'class': 'wikibase-sitelinkview-siteid'})[0]['title']
            wiki_short_lang = row.findAll('span', {'class': 'wikibase-sitelinkview-siteid'})[0].text.replace('wiki', '')
            entry = row.find('a').text
            result_tuples.append((page_title, page_id, description, langude, wiki_short_lang, entry))

    # Construct the API URL
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=pageprops&format=json'

    # Make the API request and convert the response to JSON
    response = requests.get(api_url).json()
    # Extract the page ID from the JSON response
    page = next(iter(response['query']['pages'].values()))
    if 'pageprops' in page:
        page = next(iter(response['query']['pages'].values()))['pageprops']
        # Test if the id exsists in wikibase
        if 'wikibase_item' in page:
            p_id = next(iter(response['query']['pages'].values()))['pageprops']['wikibase_item']
            base_page_id.append(p_id)
            get_wikidata_info(p_id)


extract_names_from_url(wiki_url)

all_names.remove('Given name')
all_names.remove('Template:R from given name')
all_names.remove('List of most popular given names')
all_names.remove('Onomancy')

extract_names_from_url(surnames_url)

all_names.remove('Name blending')
all_names.remove('One-name study')
all_names.remove('Template:R from surname')
all_names.remove('Template:Surname')

for name in tqdm(all_names):
    make_data_set_tupple(name)

results_df = pd.DataFrame(result_tuples, columns=['Label', 'WikiDate ID', 'English Description', 'Language', 'Wiki Short Lang', 'Entry'])
results_df.to_csv('names.csv', index=False, encoding='utf-8-sig')