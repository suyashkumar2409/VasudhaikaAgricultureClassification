from bs4 import BeautifulSoup
import requests
import os
import codecs
import json
import re

val = 0

def getPath():
    return "/home/suyash/Desktop/Agriculture"

def pathconcat(path1,folder):
    return path1+ "/" + folder

def adddirectory(currpath):

    newpath = currpath

    if not os.path.exists(newpath):
        os.makedirs(newpath)


def makefile(name,body,currpath):
    file = codecs.open(pathconcat(currpath,name), "a", "utf-8")
    #file = os.open(pathconcat(currpath,name), os.O_APPEND)
    file.write(body)
    #print(body)
    file.close()

def urlconcat(base,sub):
    return base+sub

def scrape(startingurl,foldername,lim):
    item = foldername
    #print("Created folder "+foldername)
    currurl = startingurl
    folderpath = pathconcat(getPath(),foldername)
    adddirectory(folderpath)
    print("Created folder " + foldername)
    i=0
    goon = True
    while goon:
        #print("bla")
        dmoz = requests.get(currurl)
        dmozsoup = BeautifulSoup(dmoz.content)

        alldivs = dmozsoup.find_all('div','title-and-desc')
        if alldivs:
            pass
        else:
            alldivs = 	(dmozsoup.find_all('div','site-item'))
        #print(alldivs)

        for div in alldivs:
            try:
                link = div.find_all('a')[0]['href']
                foo = requests.get(link)
                linkpage = BeautifulSoup(foo.content)
                #print(link)
                [s.extract() for s in linkpage(['style', 'script', '[document]', 'head', 'title'])]
                visible_text = linkpage.getText()
                text = visible_text
                filname = pathconcat(foldername,str(i))

                file = {"text":text, "url":link}

                with open(filname+'.json', 'w') as fp:
                    json.dump(file, fp)

                #makefile(str(i),text,folderpath)
                print("*****Scraped website "+str(i)+"of "+item)
                i = i+1
                
            except:
                continue

        if i>=lim:
            goon = False
        else:
            currurl = pathconcat("http://www.dmoz.org",dmozsoup.find_all('a', 'next-page')[0]['href'])

def main():
    ##Agri
    #scrape("http://www.dmoz.org/search?q=agriculture","Agriculture")
    #News
    lis = ['Shopping','Society','Sports','Kids & Teens Directory']
    for item in lis:
        scrape("http://www.dmoz.org/search?q="+item+"&start=0"+"&type=next&all=no&t=null&cat=", item,20000/len(lis))


main()
