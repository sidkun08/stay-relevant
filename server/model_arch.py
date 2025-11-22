import torch
import torch.nn as nn

class PolyRegress(nn.Module):
    def __init__(self, degree):
        super(PolyRegress, self).__init__()
        self.linear = nn.Linear(degree, 1)

    def forward(self, x_poly):
        return self.linear(x_poly)

def transformToTensor(data):
    global useDataStd, useDataMean
    useData = torch.tensor(data, dtype=torch.float32).unsqueeze(1)
    useDataMean = useData.mean()
    useDataStd = useData.std()
    useData = (useData - useDataMean)/useDataStd
    return useData

def normalize(pred):
    useData = pred
    useData = (useData*useDataStd) + useDataMean
    return useData
    
def polynomial_func(x, degree):
    X_poly = torch.cat([x ** i for i in range(1, degree + 1)], dim=1)
    return X_poly