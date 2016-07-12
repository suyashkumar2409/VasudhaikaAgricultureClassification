import pickle
import sklearn
import requests
import re
from get import internationalCurrency
from bs4 import BeautifulSoup

start = 0
size = 100


def getdatafromapi(b,c):
	obj = internationalCurrency(resource = '/webapi/services/urlListWithCountry/'+"India"+'?start='+str(b)+'&size='+str(c))
	#print("jheej")
	obj.createConnection()
	#print("connecr")
	retobj = obj.getUrl()
	return retobj
    
def openobject(filename):
	with open(filename, 'rb') as input:
		return pickle.load(input)


import string


def removepunctuation(x):
	# x = x.replace('.',' ')
	# x = x.replace(')',' ')
	# x = x.replace('(',' ')
	replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
	x = x.translate(replace_punctuation)
	# retstr = x.translate(string.maketrans("",""), string.punctuation)
	return x


def removeunicode(x):
	return re.sub(r'[^\x00-\x7F]+', ' ', x)


def lowercasestring(x):
	return x.lower()


def removedigits(s):
	s = re.sub(" \d+", " ", s)
	return s


def cleanstring(x):
	# x=replaceredundancy(x)
	# x=removepunctuation(x)
	x = removeunicode(x)
	# x = trimstring(x)
	x = removedigits(x)
	x = lowercasestring(x)
	return x


def getprediction(site,model,vect,ch2):
	site = site[1:-1]
	iswww = re.search(r'http://www',site)
	if iswww:
		pass
	else:
		site = site[:7]+"www."+site[7:]
	print(site)
	try:
		website = requests.get(site)
		soup = BeautifulSoup(website.content)
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	except:
		return None
	text = soup.getText()
	temp = re.sub(r'[\n\t\r ]+', " ", text)
	temp= re.sub(r'\s+'," ",temp)
	temp =  re.sub(r'\s+'," ",temp)
    
	temp = cleanstring(temp)
    
	lis = []
	lis.append(temp)
	#print(temp)
	feature_text = vect.transform(lis)
	feature_text = ch2.transform(feature_text)
    
    
	pred = model.predict(feature_text)
	print(pred)
	return pred

def main():
	model = openobject('model.pkl')
	vect = openobject('vect.pkl')
	ch2 = openobject('ch2.pkl')
	
	
	retobj = ""
	i=start
	j=0
	truepost = internationalCurrency(resource = '/webapi/services/urlListWithLanguage/classification?isInterested=1')
	falsepost = internationalCurrency(resource = '/webapi/services/urlListWithLanguage/classification?isInterested=0')
	#print("temp")
	while True:
		retobj = getdatafromapi(i,size)
		#print("here")
		j=i
		if retobj:
			print("2")
			truelist=[]
			falselist=[]
			retobj = retobj[1:-1]
			listofurl = [x.strip() for x in retobj.split(',')]
			#print(listofurl)

			for url in listofurl:
				tempurl = url
				pred = getprediction(url,model,vect,ch2)
				if pred=="Agriculture":
					truelist.append(tempurl)
				else:
					falselist.append(tempurl)
					
				j = j+1
				print(j)
				print("Not mod"+tempurl)
				with open('log','w') as f:
					f.write('j')
			if(len(truelist)>0):
				truepost.postUrl(str(truelist))
			if(len(falselist)>0):
				falsepost.postUrl(str(falselist))
		else:
			break
		#print(i)
				
						
		i = i+size
			
	
def main2():
	obj = internationalCurrency(resource = '/webapi/services/urlListWithLanguage/classification?isInterested=1')
	obj.createConnection()
	obj.postUrl("['erfef']")
	
	
main()
	
	
