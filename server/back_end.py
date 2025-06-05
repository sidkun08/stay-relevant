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
avg_vals = {}

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


def clean_files(file_name, listofCols):
    file_values = pd.read_csv(file_name, header=0)
    for col in listofCols:
        if col == 'observation_date':
            for i in file_values[col]:
                x = i.split('-')
                years.append(x[0])
        else:
            file_values[col] = file_values[col].replace(',','')
            file_values =  file_values.dropna()
            file_values[col] = pd.to_numeric(file_values[col], errors='coerce')
            values_in_file.append(file_values[col])
    
    for i in values_in_file:
        for j in i:
            values_to_use.append(j)
    

clean_files('stay-relevant/data/gdp_vals.csv', ['observation_date', 'GDP'])

for i in range(len(years)):
    first_index = i-2
    second_index = i-5
    if years[first_index] == years[second_index]:
        for i in range(len(values_to_use)):
            if i % 4 == 0:
                avg_vals[years[i]] = (sum)
                sum = 0
            sum = round((sum + values_to_use[i]), 2)

for i in range(len(years)):
    y_vals = avg_vals.values()
    x_vals = avg_vals.keys()
    plota.plot(x_vals, y_vals)
    
plota.show()

