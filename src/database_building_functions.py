from bs4 import BeautifulSoup as bs
import pandas as pd
from requests import get as re_get


def scrape_wiki_table(site, output_path):
    """
    Get the genre table, save to a csv
    :param site: wikipedia entry with a table to scrape (this case chord progressions)
    :return: df of table
    """
    # get beautiful soup and requests stuff rolling

    page = re_get(site)

    # Then get the whole page content via BS lol
    soup = bs(page.content, 'html.parser')

    # find the sortable table that has list
    # two class options for table is in html:  'wikitable sortable' or 'sortable wikitable'
    site_table = soup.find('table', {'class': 'wikitable sortable'})
    if site_table == None:
        site_table = soup.find('table', {'class': 'sortable wikitable'})
    # convert list to dataframe: https://stackoverflow.com/questions/66824674/scraping-wikipedia-table-what-am-i-missing-pandas-beautiful-soup
    # need to retain the links for artists and songs somehow (2021-09-19)
    # need to add columns for genres....somehow get the link from each song/artist to get their genres
    print(soup)
    print(site_table)
    df = pd.read_html(str(site_table))
    df = pd.DataFrame(df[0])

    # CHANGE em-dash to dash for output lol
    try:
        df['Progression'] = [x.replace('–', '-') for x in df['Progression'].tolist()]
    except KeyError:
        pass

    df.to_csv(output_path, encoding='utf-8')

    return df

