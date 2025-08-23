import requests
import pandas as pd
import matplotlib.pyplot as plota
import math
import torch
import torch.nn as nn
import torch.optim as optim
import numpy
from model_arch import PolyRegress

urls = ['https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1947-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PCE&scale=left&cosd=1959-01-01&coed=2025-05-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1959-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PPIACO&scale=left&cosd=1913-01-01&coed=2025-05-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1913-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=1947-01-01&coed=2025-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1947-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=UNRATE&scale=left&cosd=1948-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1948-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FPCPITOTLZGUSA&scale=left&cosd=1960-01-01&coed=2024-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1960-01-01']
file_names = ['stay-relevant/data/cpi_total_monthly.csv', 'stay-relevant/data/pce_total_monthly.csv', 'stay-relevant/data/ppi_total_monthly.csv', 'stay-relevant/data/gdp_total_quarterly.csv', 'stay-relevant/data/unemployement_rate_monthly.csv', 'stay-relevant/data/inflation_rate_annually.csv']

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


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

    elif "monthly.csv" in file_name:
        num = 0
        while num < len(cummalitive_yrs):
            index = cummalitive_yrs[num]
            if num % 12 == 0:
                unique_yrs.append(index)
            num += 1
        
        count = 0
        for i in cummalitive_yrs:
            if i == '2025':
                count += 1
        
        num = 0
        sum = 0
        while num < (len(unique_yrs)*12):
            if num % 12 == 0 and num != 0:
                unique_vals.append(round(((sum/12)), 4))
                sum = 0
            sum += all_vals[num]
            num += 1


        idx = -1
        count = -count
        sum = 0
        while idx >= count:
            val_for_out = all_vals[idx]
            sum += val_for_out
            idx -= 1
        unique_vals.append(round((sum/abs(count)), 4))

        print(len(unique_yrs))
        print(len(unique_vals))

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
        
        
        updated_df = pd.DataFrame({'YEARS': unique_yrs, 'VALUES': unique_vals})
        updated_df.to_csv(file_name, index=False)
    
    
def graph(file_name):
    df = pd.read_csv(file_name, header=0)
    x_var = df['YEARS']
    y_var = df['VALUES']

    plota.scatter(x_var, y_var)
    plota.show()
    
def instantiate_model(file_name):
    df = pd.read_csv(file_name, header=0)
    x = torch.tensor(df['YEARS'].values, dtype=torch.float32).unsqueeze(1)
    x_mean = x.mean()
    x_std = x.std()
    x = (x-x_mean) / x_std
    y = torch.tensor(df['VALUES'].values, dtype=torch.float32).unsqueeze(1)
    y_mean = y.mean()
    y_std = y.std()
    y = (y-y_mean)/y_std
    
    
    degree = 5
    X_poly = torch.cat([x ** i for i in range(1, degree + 1)], dim=1)

    model = PolyRegress(degree)
    cost = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

    epochs = 10000
    for epoch in range(epochs):
        model.train()
        y_pred = model(X_poly)
        loss = cost(y_pred, y)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # if epoch % 100 == 0:
            # print(f"Epoch {epoch}: Loss = {loss.item():.4f} ")
    
    model.eval()
    with torch.no_grad():
        y_pred = model(X_poly)
    
    prediction = []
    arr = y_pred.numpy()
    for i in arr:
        for j in i:
            j = (j * y_std)+y_mean
            prediction.append(j)
    
    x_arr = x.numpy()
    x_vals = []
    for i in x_arr:
        for j in i:
            j = (j * x_std) + x_mean
            x_vals.append(j)
            

    
    # for i in prediction:
        # print(i)
    
    print(file_name)
    for i in x_arr:
        print(i)        

    x = (x*x_std) + x_mean
    y = (y*y_std) + y_mean
    
    plota.scatter(x.numpy(), y.numpy(), label='Original')
    plota.plot(x.numpy(), prediction, color='red', label='Prediction')
    
    
    plota.show()


def file_manipulation():
    global urls, file_names
    for i in range(len(urls)):
        download_files(urls[i], file_names[i])
        change_file_data(file_name=file_names[i])
        # graph(file_name=file_names[i])
        instantiate_model(file_names[i])

file_manipulation()

