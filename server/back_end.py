import requests
import pandas as pd
import matplotlib.pyplot as plota


urls = [
    'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FPCPITOTLZGUSA&scale=left&cosd=2000-01-01&coed=2025-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-06-23&revision_date=2025-06-23&nd=1960-01-01',
    'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=2000-01-01&coed=2024-10-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-06-23&revision_date=2025-06-23&nd=1947-01-01'
]
file_names = ['stay-relevant/data/inflation.csv', 'stay-relevant/data/gdp.csv']


def download_files(file_url, file_path):
    downloading = requests.get(url=file_url)
    if downloading.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(downloading.content)
        print("Great")
    else:
        print('Trash')

def change_file_data(file_name):
    orginal = []
    vals = []
    true_vals = []
    df = pd.read_csv(file_name, header=0)
    if 'observation_date' in df:
        print( "Amazing")
        print(df['observation_date'])
        for i in df['observation_date']:
             years = i.split('-')
             orginal.append(int(years[0]))
    
    for i in df:
        if i != 'observation_date':
            for j in df[i]:
                vals.append(j)

    newdf = pd.DataFrame({'YEARS': orginal})
    years = (newdf['YEARS'].unique())
    
    if file_name == 'stay-relevant/data/gdp.csv':
        sum = 0
        num = 0
        for i in vals:
            sum += i
            num += 1
            if num % 4 == 0:
                true_vals.append((sum/4))
                sum = 0
    else:

       for i in vals:
           true_vals.append(i)
    
    new_dataFrame = pd.DataFrame({'years': years, 'values': true_vals})
    new_dataFrame.to_csv(file_name, index=False)

def graph(file_name):
    df = pd.read_csv(file_name, header=0)
    x_var = df['years']
    y_var = df['values']

    plota.scatter(x_var, y_var)
    plota.show()

def linear_regress(file_name):
    return None
def send_files():
    global urls, file_names
    for i in range(len(urls)):
        download_files(urls[i], file_names[i])
        change_file_data(file_name=file_names[i])
        graph(file_name=file_names[i])

send_files()

