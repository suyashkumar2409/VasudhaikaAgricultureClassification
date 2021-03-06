import requests
import json
import logging
import httplib
import time
import urllib as urllib2
import re

class internationalCurrency():
    
    def __init__(self, host='192.168.1.118', port=8080, resource='/webapi/services/urlListWIthLanguage', url=''):
        logging.info("test")
        self.host = host
        self.port = port
        self.resource = resource
        if url:
            self.url = url
        else:
            self.url = ('http://%s:%s%s') % (host, port, resource)

    def createConnection(self):
        logging.info("inside create connection...........")
        try:
            print(self.url)
            self.conn = urllib2.request.urlopen(self.url)
            print(self.conn)
        except httplib.HTTPException:
            raise
        except httplib.NotConnected:
            raise
        except httplib.ImproperConnectionState:
            raise
        except:  # TODO To many things could possibly go wrong. So we catch all.
            message = (u'Unable to connect Content Server ,' +
                       'make sure it is running using service Content status')
            logging.info(message)
    
            
    def getUrl(self):
        try:
        	response = requests.get(self.url)
        	print(self.url)
        	return (response.content)           
        except:
            print ("error")
            
    def postUrl(self,args):
        try:
            print self.url
            response=requests.post(self.url,args)
            print response.content
            print("happened")
            print response
        except :
            print "error"

    def printResponse(self):
        try:
		#print "e"+self.url
            response = requests.get(self.url)
    		#print response
            if response.content:
                    	url = response.content
                    	print (url)
            else:
                logging.info("\n International Currency is not getting...")
        except:
            print ("error")

   
if __name__ == "__main__":
    a = str(input())
    b = input()
    c = input()
    obj = internationalCurrency(resource = '/webapi/services/urlListWithLanguage/'+"en"+'?start='+b+'&size='+c)
    obj.createConnection()
    obj.getUrl()
