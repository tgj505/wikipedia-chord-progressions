import matplotlib.pyplot as plt
from src.plotting_functions import plot_bar_with_rolling_mean
from src.data_loading import load_table_csv, get_year_list
from src.database_building_functions import scrape_wiki_table
from config.config import DATA_PATH


# scrape and save table as csv
# site, csv_path = 'https://en.wikipedia.org/wiki/%2750s_progression',\
#                 DATA_PATH / 'wiki-50s_progression.csv'
# site, csv_path = 'https://en.wikipedia.org/wiki/I–V–vi–IV_progression',\
#                 DATA_PATH / 'wiki-I-V-vi-IV_progression.csv'
site, csv_path = 'https://en.wikipedia.org/wiki/IV%E2%96%B37%E2%80%93V7%E2%80%93iii7%E2%80%93vi_progression', \
                 DATA_PATH / 'wiki-IV△7–V7–iii7–vi_progression.csv'

scrape_wiki_table(site=site, output_path=csv_path)


# load and format the data to graph:
df = load_table_csv(csv_path)
year_list = get_year_list(df)

# add bar of song count along with the rolling mean of +=n years
ax1 = plot_bar_with_rolling_mean(year_list, n=3, progression_name=str(csv_path).split('.csv')[0].split('data\\')[1])

# display/save
plt.show()





