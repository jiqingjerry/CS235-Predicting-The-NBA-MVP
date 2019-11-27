import csv
import numpy as np
import torch 
from torch.utils.data import Dataset, random_split

def ProcessCSV(file):
    results = []
    #open csv file
    datafile = open(file, 'r')
    myreader = csv.reader(datafile)
    for row in myreader:
        results.append(row)
    #the features are the first row of the csv file
    features = np.array([s.lower() for s in results[0]])
    data = np.array(results[1:])
    return features, data  

class NBADataset(Dataset):
    def __init__(self, csvFile, featureNames): 
        features, data = ProcessCSV(csvFile)
        #get index for our label
        idx = np.where(features == featureNames['label'])
        idx2 = np.where(features == 'player')
        #get corresponding column
        self.awdShare = data[:,idx].astype(float)
        self.playerNames = data[:,idx2]

        #create empty array to hold features we care about
        self.data = np.zeros(shape=(self.awdShare.shape[0],1))
        #extract feature columns
        for name in featureNames['features']:
            index = np.where(features == name)
            self.data = np.append(self.data, data[:,index].astype(float).reshape(-1,1), axis=1)
        #delete 0 column
        self.data = np.delete(self.data,0,axis=1)

    def __len__(self):
        return len(self.data)

    def __getitem__(self,idx):
        sample = self.data[idx,:]
        label = self.awdShare[idx]
        return torch.Tensor(sample), label
    
    def getPlayerName(self,idx):
        return self.playerNames[idx].item()

def SplitDataSet(dataset, split):
    testSize = int(split * len(dataset))
    trainSize = len(dataset) - testSize
    return random_split(dataset, [trainSize, testSize])