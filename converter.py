import pandas as pd
import numpy as np
import os
import codecs
import json
import re


def getPath():
    return "/home/suyash/Desktop/Agriculture"


def getFolders():
    return os.listdir(getPath())


def joinPath(path1, path2):
    return str(path1) + "/" + str(path2)


def getfilename(foldername, articlenum):
    f = joinPath(getPath(), foldername)
    f = joinPath(f, articlenum)
    f += '.json'
    return f


def clean_text(text):
    temp = re.sub(r'[\n\t\r ]+', " ", text)
    temp= re.sub(r'\s+'," ",temp)
    return re.sub(r'\s+'," ",temp)


def getRow(foldername, articlenum, category):
    columns = ['Category', 'Url', 'Text']
    filename = getfilename(foldername, articlenum)
    with open(filename, 'r') as fp:
        data = json.load(fp)
    #####read json here
    formattedtext = clean_text(data['text'])
    dic = {'Category': category, 'Text': formattedtext, 'Url': data['url']}

    return pd.DataFrame(dic, columns=columns, index=[0])


def main():
    print("yo")
    temp = 0
    listfolders = ['Agriculture','News']
    print listfolders
    # columns = ['Category', 'Text']
    mydataframe = pd.DataFrame()
    for folder in listfolders:
        temp = 0
        articlenum = 0
        print("*****Folder " + folder + " started")
        #while (temp <= 5):
        while(os.path.isfile(getfilename(folder, articlenum))):
            # category = folder.replace("_farms", '')
            category = folder
            mydataframe = mydataframe.append(getRow(folder, articlenum, category), ignore_index=True)
            articlenum = articlenum + 1
            temp = temp + 1
            print("Added article " + str(articlenum) + " of folder " + folder)
            if (folder == 'News' and articlenum >= 39000):
                break
        print("*****Folder " + folder + " completed")

    mydataframe.to_csv('data_small.csv', index=False, encoding='utf-8')


main()
