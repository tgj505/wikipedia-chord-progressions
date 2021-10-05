from pandas import read_csv


def load_table_csv(file):
    return read_csv(file)


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

