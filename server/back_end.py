import requests
import pandas as pd
import matplotlib.pyplot as plota


urls = [
    'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=2000-01-01&coed=2025-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-06-01&revision_date=2025-06-01&nd=1947-01-01',
    'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FPCPITOTLZGUSA&scale=left&cosd=2000-01-01&coed=2024-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-06-01&revision_date=2025-06-01&nd=1960-01-01',
]
file_names = ['stay-relevant/data/gdp_vals.csv', 'stay-relevant/data/inflation_vals.csv']

years = []
values_in_file= []
values_to_use = []

stuff = {}


sum = 0
counter = 0

def download_files(file_url, file_path):
    downloading = requests.get(url=file_url)
    if downloading.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(downloading.content)
        print("Great")
    else:
        print('Trash')

def send_files():
    global urls, file_names
    for i in range(len(urls)):
        download_files(urls[i], file_names[i])
