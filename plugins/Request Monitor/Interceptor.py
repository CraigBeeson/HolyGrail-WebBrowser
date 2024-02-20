import datetime
import re
import socket
import requests
from PyQt5.QtWebEngineCore import *
from . import Predict
from .NeuralNetwork import NeuralNetwork

"""
Just a thrown together integration of AI I found by someone else that
detects malicious connections, but is based on server side and
just says all connections are suspicious, but thats to be expected
"""

paths = ["/login", "/phpmyAdmin/", "/phpmyadmin2012/", "/pma2013", "/pma2018", "/phpmyadmin2013/", "/phpmyadmin2", "/mysql/web/",
"/PMA2015", "/administrator/web", "/PMA2012", "/sql/webadmin", "/pma2011", "/pma2014", "/pma2017", "/PMA2014", "/phpmyadmin2011/",
"/phpmyadmin2015/", "/phpmyadmin2017/", "/PMA2017", "/PMA2013", "/sql/phpMyAdmin/", "/pma2016", "/mysqlmanager", "/administrator/admin",
"/2phpmyadmin", "/administrator/phpmyadmin", "/phpmyadmin2018/", "/search"]

class Interceptor(QWebEngineUrlRequestInterceptor):
	
	def __init__(self,parent):
		super(Interceptor, self).__init__(parent)
	
	def interceptRequest(self, info):
		#processes request information to fit the AI json input
		request = (requests.get(info.requestUrl().toString()))
		timestamp = int(datetime.datetime.now().timestamp()*1000)
		method = str(info.requestMethod(),encoding="utf-8").lower()
		query = info.requestUrl().toString()
		query = re.search("search\\?.*?&",query)
		if query == None:
			query = ""
		else:
			query = str(query.group())
			query = re.sub("search\\?q=","",query)
			query = re.sub("search\\?q","",query)
			query = re.sub("&","",query)
			query = re.sub("\\+"," ",query)
			query = "\"" + query + "\""
			if query == "\"\"":
				query = ""
			else:
				query = "\"query\":"+ query
		path = info.requestUrl().toString()
		knownPath = False
		for i in paths:
			if i in path:
				path = i
				knownPath = True
				break
		if knownPath:
			pass
		else:
			path = "/home"
		source = re.search("/.+?/",info.requestUrl().toString()).group()
		source = source.strip("/")
		head = requests.head("https://"+source)
		try:
			payload = re.search("<title>.*?</title>",str(requests.get(info.requestUrl().toString()).content)).group()
			payload = re.sub("<title>","",payload)
			payload = re.sub("</title>","",payload)
		except:
			payload = ""
		status = head.status_code
		head.headers = {u'Report-To': "None"}
		head = re.sub("\'","\"",str(head.headers))
		source = socket.gethostbyname(source)
		test = "|{\"timestamp\":" + str(timestamp) + ",\"method\":\"" + method + "\",\"query\":{" + query + "},\"path\":\"" + path + "\",\"statusCode\":" + str(status) + ",\"source\":{\"remoteAddress\":\"" + source + "\",\"referer\":\"http://localhost:8002\"},\"route\":\"" + path + "\",\"headers\":" + head + ",\"responsePayload\":\"" + payload + "\"}|"
		file = "Data/securitai.csv"
		with open(file, 'w') as f:
			f.write(test)
			f.close()
		#get the prediction
		passVar = Predict.predict(file,"0")