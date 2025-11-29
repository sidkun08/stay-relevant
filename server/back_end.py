import requests
import pandas as pd
import matplotlib.pyplot as plota
import torch
import torch.nn as nn
import torch.optim as optim
from model_arch import PolyRegress, transformToTensor, polynomial_func, normalize, getMean, getStd
import json
from flask import Flask

app = Flask(__name__)

urls = ['https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1947-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PCE&scale=left&cosd=1959-01-01&coed=2025-05-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1959-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PPIACO&scale=left&cosd=1913-01-01&coed=2025-05-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1913-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=1947-01-01&coed=2025-01-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-15&revision_date=2025-07-15&nd=1947-01-01',
        'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PINCOME&scale=left&cosd=1947-01-01&coed=2025-04-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-11-25&revision_date=2025-11-25&nd=1947-01-01']
file_names = ['data/cpi_total_monthly.csv', 'data/pce_total_monthly.csv', 'data/ppi_total_monthly.csv', 'data/gdp_total_quarterly.csv', 'data/income_total_quarterly.csv']

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

num=0
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

        updated_df = pd.DataFrame({'YEARS': unique_yrs, 'VALUES': unique_vals})
        updated_df.to_csv(file_name, index=False)

    elif 'quarterly' in file_name:
        num = 0
        for i in cummalitive_yrs:
            if num % 4 == 0:
                unique_yrs.append(i)
            num += 1

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
    plota.title(label=file_name)
    plota.show()
    
def instantiate_model(file_name):
    global user_input, model, x_test, y_test, x_test_data, y_test_data, cost, degree, getAccurate, num
    df = pd.read_csv(file_name, header=0)
    x_train_data = []
    x_test_data = []
    y_train_data = []
    y_test_data = []
    getAccurate = []

    num1 = 0.85

    lengthOftrain = len(df['YEARS'])
    lengthOftrain = lengthOftrain*num1
    lengthOftrain= round((lengthOftrain))
    lengthOftrain = int(lengthOftrain)


    for i in df['YEARS']:
        x_train_data.append(i)
        if len(x_train_data) == lengthOftrain:
            true_max = x_train_data[lengthOftrain-1]
            true_max = x_train_data.index(true_max)
            break
    get_indexList = []
    for i in df['YEARS']:
        get_indexList.append(i)
        if get_indexList.index(i) >= true_max:
            x_test_data.append(i)
    for j in df['VALUES']:
        y_train_data.append(j)
        if len(y_train_data) == lengthOftrain:
            true_max = y_train_data[lengthOftrain-1]
            true_max = y_train_data.index(true_max)
            break
    get_indexList = []
    for j in df['VALUES']:
        get_indexList.append(j)
    for i in get_indexList:
        val = get_indexList.index(i)
        if val >= true_max:
            y_test_data.append(i)
    
    print(x_train_data)
    print(x_test_data)
    
    x_train = transformToTensor(x_train_data)
    y_train = transformToTensor(y_train_data)

    x_test = transformToTensor(x_test_data)
    y_test = transformToTensor(y_test_data)
    
    
    degree = 5
    X_Train_Func = polynomial_func(x_train, degree)

    model = PolyRegress(degree)
    cost = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    epochs = 20000
    for epoch in range(epochs):
        model.train()
        y_pred = model(X_Train_Func)
        loss = cost(y_pred, y_train)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"Epoch {epoch}: Loss = {loss.item():.4f} ")
    print(f"Training Prediction Data:\nAccuracy: {loss}")
    y_pred = normalize(y_pred, y_train_data)
    for i in range(len(y_pred)):
        tensorVal = y_pred[i]
        tensorVal = tensorVal.item()
        print(tensorVal)
    
    model_save_path = f"model{num}.pth"
    torch.save(model.state_dict(), model_save_path)
    num += 1
    return model_save_path


def runModel(path_name, file_name):
    degree = 5
    model = PolyRegress(degree)
    cost = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    model.load_state_dict(torch.load(path_name))
    model.eval()
    with torch.no_grad():
        X_Test_Func = polynomial_func(x_test, degree)
        y_test_pred = model(X_Test_Func)
        loss = cost(y_test_pred, y_test)

    y_test_pred = normalize(y_test_pred, y_test_data)
    print("Testing Prediction Data:\n")
    for i in range(len(y_test_pred)):
        tensorVal = y_test_pred[i]
        tensorVal = tensorVal.item()
        getAccurate.append(tensorVal)
        print(tensorVal)

    with torch.no_grad():
        user_input = 2026
        data = [user_input]
        custom_tensor = torch.tensor(data, dtype=torch.float32).unsqueeze(1)
        _mean = getMean(x_test_data)
        _std = getStd(x_test_data)
        stan = (custom_tensor - _mean) / _std
        func = polynomial_func(stan, degree)
        run = model(func)
        given_pred = normalize(run, y_test_data)

    for i in range(len(given_pred)):
        myVal = given_pred[i]
        myVal = myVal.item()

    main_dict = {file_name: [{user_input: myVal}]}
    with open('data/predicted_data.json') as file:
        file_read = json.load(file)
    for entry in file_read:
        for name in entry:
            if file_name in name:
                file_read.remove(entry)

    with open('data/predicted_data.json', 'w') as file:
        json.dump(file_read, file)
    file.close()

    with open('data/predicted_data.json') as file:
        loaded = json.load(file)

    loaded.append(main_dict)

    with open('data/predicted_data.json', 'w') as file:
        json.dump(loaded, file, indent=4, separators=(", ", ": "))
    file.close()
            

@app.route('/')
def file_manipulation():
    global urls, file_names
    for i in range(len(file_names)):
        download_files(urls[i], file_names[i])
        change_file_data(file_name=file_names[i])

@app.route('/run')
def run_model():
    num = 0
    for i in range(len(file_names)):
        runModel(f"model{num}.pth", file_names[i])
        num +=1

@app.route('/conclude')
def compare(JSONFile):
    global user_input
    vals = []
    max_val = []
    predicted_va = []
    isIncreasing = False
    for idx in range(len(file_names)):
        vals.clear()
        true_file = file_names[idx]
        df = pd.read_csv(true_file, header=0)
        for i in df['VALUES']:
            vals.append(i)
        max_val.append(max(vals))
        with open(JSONFile) as file:
            load = json.load(file)
        for entry in load:
            for name in entry:
                names = entry.get(name)
                for num in names:
                    y = num.values()
                    for val in y:
                        the_val = val
                        predicted_va.append(val)
    isIncreasing = []
    isDecreasing = []
    for i in range(len(file_names)):
        target = predicted_va[i]
        maximum = max_val[i]
        if 'cpi' in file_names[i]:
            inflation = (((target - maximum) / (maximum))*100)
        difference = (((target-maximum) / (maximum)) * 100)
        if difference > 0:
            dictDifference = {file_names[i]: difference}
            isIncreasing.append(dictDifference)
        else:
            dictDifference = {file_names[i]: difference}
            isDecreasing.append(dictDifference)
    inflationCount = {'inflationForPredicted': f"{inflation}%"}
    with open('data/conclusions.json') as file:
        loaded = json.load(file)
    for entry in loaded:
        for i in entry:
            key = i.keys()
            for name in key:
                if name in file_names:
                    loaded.clear()
    with open('data/conclusions.json', 'w') as file:
        json.dump(loaded, file, indent=4)
    file.close()

    with open('data/conclusions.json') as file:
        listOfConclusion = json.load(file)
    
    listOfConclusion.append(isIncreasing)
    listOfConclusion.append(isDecreasing)

    with open('data/conclusions.json', 'w') as file:
        send = json.dump(listOfConclusion, file, indent=4, separators=(', ', ': '))
    
    file.close()

    with open('data/conclusions.json') as jfile:
        everything = json.load(jfile)            

    statements = []
    EconIsIncreasing = 0
    finalStatement = ""
    for i in isIncreasing:
        name = [name for name in i]
        name = name[0].split('/')[1].split('_')[0]
        name = name.upper()

        value = [val for val in i.values()]
        value = value[0]
        if value > 0:
            statement = f'The {name} has increased by {round(value, 2)}%. This signifies a positive increase to the economy.\n'
            statements.append(statement)
            EconIsIncreasing += 1
        elif value < 0:
            statement = f'The {name} has decreased by {round(value, 2)}%. This signifies a negative decrease to the economy.\n'
            statements.append(statement)
            EconIsIncreasing -= 1
        else:
            statement = f'The {name} has increased by {round(value, 2)}%. This signifies a positive increase to the economy.\n'
            statements.append(statement)
            EconIsIncreasing += 1

    if inflation > 0:
        statement = f'The inflation has increased by {round(inflation, 2)}%. This signifies a negative decrease to the economy.\n'
        statements.append(statement)
        EconIsIncreasing -= 1
    elif inflation < 0:
        statement = f'The inflation has decreased by {round(inflation, 2)}%. This signifies a positive increase to the economy.\n'
        statements.append(statement)
        EconIsIncreasing += 1
    else:
        statement = f'The inflation has increased by {round(inflation, 2)}%. This signifies a positive increase to the economy.\n'
        statements.append(statement)
        EconIsIncreasing += 1
    
    if EconIsIncreasing > 0:
        concludingStatement = 'In Conclusion, the economy is in a good place in the provided year.'
        statements.append(concludingStatement)
    elif EconIsIncreasing < 0:
        concludingStatement = 'In Conclusion, the economy is not in a good place in the provided year.'
        statements.append(concludingStatement)
    else:
        concludingStatement = 'In Conclusion, the economy is in a good place in the provided year.'
        statements.append(concludingStatement)

    for i in range(len(statements)):
        finalStatement += statements[i]
    print(finalStatement)

file_manipulation()
run_model()
compare('data/predicted_data.json')