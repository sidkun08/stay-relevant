import requests
import pandas as pd
import matplotlib.pyplot as plota
import math


urls = ['https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1947-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PCE&scale=left&cosd=1959-01-01&coed=2025-05-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1959-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PPIACO&scale=left&cosd=1913-01-01&coed=2025-05-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1913-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=1947-01-01&coed=2025-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1947-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=UNRATE&scale=left&cosd=1948-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1948-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FPCPITOTLZGUSA&scale=left&cosd=1960-01-01&coed=2024-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1960-01-01']
file_names = ['stay-relevant/data/cpi_total_monthly.csv', 'stay-relevant/data/pce_total_monthly.csv', 'stay-relevant/data/ppi_total_monthly.csv', 'stay-relevant/data/gdp_total_quarterly.csv', 'stay-relevant/data/unemployement_rate_monthly.csv', 'stay-relevant/data/inflation_rate_annually.csv']


def download_files(file_url, file_path):
    downloading = requests.get(url=file_url)
    if downloading.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(downloading.content)
        print("Great")
    else:
        print('Trash')

def change_file_data(file_name):
    cummalitive_yrs = []
    unique_yrs = []
    unique_vals = []
    all_vals = []
    df = pd.read_csv(file_name, header=0)
    for col in df:
        if 'observation_date' in col:
            for i in df[col]:
                date = i
                year = date.split('-')[0]
                cummalitive_yrs.append(year)
        else:
            for i in df:
                for j in df[col]:
                    all_vals.append(j)
    num = 0
    if 'daily' in file_name:
        for i in cummalitive_yrs:
            if num % 365 == 0:
                unique_yrs.append(i)
                num +=1
        
        num = 0
        sum = 0

        for i in all_vals:
            sum += i
            if num % 365 == 0 and num != 0:
                unique_vals.append(sum/365)
                sum = 0

    elif 'monthly' in file_name:
        for i in cummalitive_yrs:
            if num % 12 == 0:
                unique_yrs.append(i)
            if i == 2025:
                unique_yrs.append(2025)
                break
            num += 1
        
        num = 0
        sum = 0
        while num < (len(unique_yrs)*12):
            sum += all_vals[num]
            num += 1
            if num % 12 == 0 and num != 0:
                unique_vals.append(round(((sum/12)), 4))
                sum = 0
        count = 0
        for i in cummalitive_yrs:
            if 2025 == i:
                count += 1
        
        if 2025 in unique_yrs:
            num = -1
            sum = 0
            while num >= count:
                if num == count:
                    unique_vals.append((sum)/6)
                    break
                val = all_vals[num]
                sum += val
                num -= 1

        print(len(unique_vals))
        print(len(unique_yrs))

        updated_df = pd.DataFrame({'YEARS': unique_yrs, 'VALUES': unique_vals})
        updated_df.to_csv(file_name, index=False)

    elif 'quarterly' in file_name:
        num = 0
        for i in cummalitive_yrs:
            if num % 4 == 0:
                unique_yrs.append(i)
            num += 1
        print(unique_yrs)

        num = 0
        sum = 0
        while num < (len(unique_yrs)*4):
            if num % 4 == 0 and num != 0:
                unique_vals.append(round(((sum/4)), 4))
                sum = 0
            sum += all_vals[num]
            num += 1
            
        if '2025' in unique_yrs:
            num = -1
            val= all_vals[num]
            unique_vals.append((val))
            
            

        print(len(unique_vals))
        print(len(unique_yrs))

        updated_df = pd.DataFrame({'YEARS': unique_yrs, 'VALUES': unique_vals})
        updated_df.to_csv(file_name, index=False)
    elif 'annually' in file_name:
        for i in cummalitive_yrs:
            unique_yrs.append(i)

        num = 0

        while num < len(unique_yrs):
            unique_vals.append(all_vals[num])
            num += 1
        
        print(len(unique_yrs))
        print(len(unique_vals))
        updated_df = pd.DataFrame({'YEARS': unique_yrs, 'VALUES': unique_vals})
        updated_df.to_csv(file_name, index=False)
    
    
def graph(file_name):
    df = pd.read_csv(file_name, header=0)
    x_var = df['YEARS']
    y_var = df['VALUES']

    plota.scatter(x_var, y_var)
    plota.show()
    

        
def send_files():
    global urls, file_names
    for i in range(len(urls)):
          download_files(urls[i], file_names[i])
          change_file_data(file_name=file_names[i])
          graph(file_name=file_names[i])
send_files()

