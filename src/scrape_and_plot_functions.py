from bs4 import BeautifulSoup as bs
import pandas as pd
from requests import get as re_get
from collections import Counter
import matplotlib.pyplot as plt


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
    df = pd.read_html(str(site_table))
    df = pd.DataFrame(df[0])

    # CHANGE em-dash to dash for output lol
    try:
        df['Progression'] = [x.replace('–', '-') for x in df['Progression'].tolist()]
    except KeyError:
        pass

    df.to_csv(output_path, encoding='utf-8')

    return df


def get_year_list(df):
    # counts items reappearing in multiple years (covers/recharts)
    try:
        year_list = [x.split('/') for x in df['Year'].tolist()]
        for list_ in [list_in_year_list for list_in_year_list in year_list if type(list_in_year_list) == list]:
            year_list.remove(list_)
            for list_item in list_:
                year_list.append(list_item)
        year_list = [int(x) for x in year_list]

    except AttributeError:
        year_list = df['Year'].astype(int).tolist()
    return year_list


def plot_bar_with_rolling_mean(year_list, n, progression_name):
    """

    :param year_list: a list of years of songs to count (eg, [2020, 2021, 2019, 2020, 2020, 2018, 2015, 2015, 2014])
    :param n: rolling mean year input, + or -. (So mean "bin" is n*2+1)
    :return: ax1 as plt.bar + plt.plot of rolling mean
    """


    songs = len(year_list)



    # get bins before adding in missing years/values to do rolling mean
    i = min(year_list) - n
    rolling_dict = {}
    while i < max(year_list):
        temp_list = [x for x in year_list if i - n <= x <= i + n]
        rolling_dict[i] = len(temp_list) /(n*2+1)
        i += 1

    # fill in years with no listed songs
    """
    couldn't figure out a more elegant way to "fill" all missing dates on matplotlib, So just:
        -added 1 for every year in range from first to last
        -counted the number of each year in the list/
        -subtracted one from each
    """

    i = min(year_list)
    while i <= max(year_list):
        year_list.append(i)
        i += 1
    year_count = Counter(year_list)

    ax1 = plt.bar(year_count.keys(),
                  [x-1 for x in year_count.values()],
                  color='darkred',
                  alpha=.5)


    # now plot rolling mean
    plt.plot(rolling_dict.keys(),
             rolling_dict.values(),
             color='k',
             linestyle='--',
             linewidth=2,
             label='yearly_mean',
             )

    # stylize and label
    plt.grid(color='darkgrey',
             alpha=.7,
             )
    plt.xticks(rotation=-30,
               color='k',
               fontfamily='serif',
               )
    plt.yticks(rotation=0,
               color='k',
               fontfamily='serif',
               )
    plt.xlabel('Year',
               fontdict={'size': 10,
                         'color': 'k',
                         'fontfamily': 'serif'}
               )
    plt.ylabel('Number of Songs',
               fontdict={'size': 10,
                         'color': 'k',
                         'fontfamily': 'serif'}
               )
    plt.title(f"{songs} Songs in Wikipedia's {progression_name} list",
              fontdict={'size': 15,
                        'color': 'k',
                        'fontfamily': 'serif'},
              )
    plt.legend([f'rolling average (±{n}years)',
                'annual count']
               )

    # annotate max
    max_count = max([x-1 for x in year_count.values()])
    max_year = [year for year, count in year_count.items() if count-1 == max_count][0]
    max_bin = max([x for x in rolling_dict.values()])
    max_bin_year = [year for year, count in rolling_dict.items() if count == max_bin][0]

    plt.annotate(f'Peak: {max_year}, {max_count} songs',
                 # xytext=(max_year+3, max_count-1),
                 xy=(max_year, max_count),
                 arrowprops=dict(facecolor='grey',
                                 edgecolor='k',
                                 # shrink=2,
                                 width=1,
                                 headlength=8,
                                 headwidth=5,
                                 ),
                 )
    plt.annotate(f'Peak avg: {max_bin_year}, {round(max_bin,1)} songs',
                 xy=(max_bin_year, max_bin),
                 # xytext=(max_bin_year, max_bin),
                 arrowprops=dict(facecolor='grey',
                                 edgecolor='k',
                                 # shrink=2,
                                 width=1,
                                 headlength=8,
                                 headwidth=5,
                                 ),
                 )

    """
    plt.annotate(text=f'\'70s nostalgia',
                 xy=(1975, rolling_dict[1975]),
                 xytext=(max_bin_year+20 + 6, 3),
                 arrowprops=dict(facecolor='grey',
                                 edgecolor='k',
                                 shrink=2,
                                 width=1,
                                 headlength=8,
                                 headwidth=5,
                                 )

                 )

    plt.annotate(text=f'\'10s revival?',
                 xy=(2015, rolling_dict[2015]),
                 xytext=(2009, 5.5),
                 arrowprops=dict(facecolor='grey',
                                 edgecolor='k',
                                 shrink=2,
                                 width=1,
                                 headlength=8,
                                 headwidth=5,
                                 )

                 )

    """

    return ax1


