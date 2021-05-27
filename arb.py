from decimal import *
import time
import requests
from threading import Thread
import urllib.parse
import json
import hmac,hashlib

#bter stuff
def query(req, url):
 req['nonce'] = int(time.time()*1000)
 post_data = urllib.parse.urlencode(req)
 post_data=post_data.encode('utf-8')
 #dis for bter ^^
 sign = hmac.new(str.encode("inputpersonalkeyhere"), post_data, hashlib.sha512).hexdigest()
 headers = {'Sign': sign,'Key': "inputpersonalkeyhere"} 
 ret = requests.post(url, data = req, headers=headers)
 return ret.json()

#example of args
#ltc_btc
#SELL or BUY
#0.023
#100

def trade(pair,type,rate,amount):
	return query({"pair":pair,"type":type,"rate":rate,"amount":amount},'https://bter.com/api/1/private/placeorder')

#polo
def queryPolo(command, reqq):
 reqq['command'] = command
 reqq['nonce'] = int(time.time()*1000)
 post_data = urllib.parse.urlencode(reqq)
 post_data=post_data.encode('utf-8')
 sign = hmac.new(str.encode("inputpersonalkeyhere"), post_data, hashlib.sha512).hexdigest()
 headers = {'Sign': sign,'Key': "inputpersonalkeyhere"}
 ret = requests.post('https://poloniex.com/tradingApi', data = reqq, headers=headers)
 return ret.json()
	
def buy(currencyPair,rate,amount):
	return queryPolo('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

def sell(currencyPair,rate,amount):
	return queryPolo('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})






#input relevant 2 dicts above
def returnArbOpportunity(relevant_dict_1,relevant_dict_2):
	#rd1 relevant dict 1 , et 2 sequentially, quel echange a quel echange it's modulable , though needs to be same format of donnes from api
	rd2_asks = Decimal(relevant_dict_2[0])
	rd2_bids = Decimal(relevant_dict_2[2])
	rd1_asks = Decimal(relevant_dict_1[0])
	rd1_bids = Decimal(relevant_dict_1[2])

	
	totalbenefice = Decimal(0)
	if rd2_asks < rd1_bids:
		sellrd1buyrd2_priceunit = rd1_bids - rd2_asks
		rd2_asks_volume = Decimal(str(relevant_dict_2[1]))
		rd1_bids_volume = Decimal(str(relevant_dict_1[3]))
		
		if rd2_asks_volume <= rd1_bids_volume:
			totalbenefice = rd2_asks_volume * sellrd1buyrd2_priceunit
			#"buy from arg2 sell to arg1"
			return [totalbenefice, rd2_asks_volume, rd2_asks, rd1_bids, relevant_dict_2[4],relevant_dict_1[4]]
		elif rd2_asks_volume > rd1_bids_volume:
			totalbenefice = rd1_bids_volume * sellrd1buyrd2_priceunit		
			return [totalbenefice, rd1_bids_volume, rd2_asks, rd1_bids, relevant_dict_2[4],relevant_dict_1[4]]
		
	elif rd1_asks < rd2_bids:
		buyrd1sellrd2_priceunit = rd2_bids - rd1_asks
		rd2_bids_volume = Decimal(str(relevant_dict_2[3]))
		rd1_asks_volume = Decimal(str(relevant_dict_1[1]))
		
		if rd1_asks_volume <= rd2_bids_volume:
			totalbenefice = rd1_asks_volume * buyrd1sellrd2_priceunit
			return [totalbenefice, rd1_asks_volume, rd1_asks, rd2_bids, relevant_dict_1[4],relevant_dict_2[4]]
			
		elif rd1_asks_volume > rd2_bids_volume:
			totalbenefice = rd2_bids_volume * buyrd1sellrd2_priceunit
			return [totalbenefice, rd2_bids_volume, rd1_asks, rd2_bids, relevant_dict_1[4],relevant_dict_2[4]]	
	
	if 	totalbenefice == Decimal(0):
		return [Decimal(0)]


#start_time = time.time()




class Download(Thread):

	def __init__(self, url):
		Thread.__init__(self)
		self.url = url
		self.dict = {}

	def run(self):
		#for the hitbtc and polio dicts  
		#self.dict = json.loads(urllib.request.urlopen(self.url).read())
		self.dict = requests.get(self.url).json()


		
		
		
		
while 1==1:
	
	# Création des threads
	thread_polo_ETH = Download('https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_ETH&depth=1')


	thread_bter_ETH = Download('http://data.bter.com/api/1/depth/eth_btc')


	# Lancement des threads
	thread_polo_ETH.start()
	
	thread_bter_ETH.start()

	# Attend que les threads se terminent.join()
	thread_polo_ETH.join()

	thread_bter_ETH.join()


	
	dict = {
		"ETH": []
	}

	#bter
	
	passs = 1
	if thread_bter_ETH.dict!={}:		
		if len(thread_bter_ETH.dict["asks"])>=1 and len(thread_bter_ETH.dict["bids"])>=1:
			numberofasks_ETH = len(thread_bter_ETH.dict["asks"])
			dict["ETH"].append([Decimal(str(thread_bter_ETH.dict["asks"][numberofasks_ETH-1][0])),Decimal(str(thread_bter_ETH.dict["asks"][numberofasks_ETH-1][1])),Decimal(str(thread_bter_ETH.dict["bids"][0][0])),Decimal(str(thread_bter_ETH.dict["bids"][0][1])),"bter"])
			passs = 0

	if thread_polo_ETH.dict!={}:		
		if len(thread_polo_ETH.dict["asks"])>=1 and len(thread_polo_ETH.dict["bids"])>=1:
			dict["ETH"].append([Decimal(thread_polo_ETH.dict["asks"][0][0]),Decimal(str(thread_polo_ETH.dict["asks"][0][1])),Decimal(thread_polo_ETH.dict["bids"][0][0]),Decimal(str(thread_polo_ETH.dict["bids"][0][1])),"polo"])
			passs = 0
	#polo




	if passs == 0:
		hmm = returnArbOpportunity(dict["ETH"][0],dict["ETH"][1]) 
		if hmm[0] >= 0.002: 
			volumeboughtt = Decimal(str(0.042))/hmm[2]
			if volumeboughtt >= hmm[1]:
				if hmm[1] <= 3.18:
					print("Benefice: "+str(hmm[0])+" /volume bought "+str(hmm[1])+" /ask price "+str(hmm[2])+" /bid price "+str(hmm[3])+" /buy from: "+hmm[4]+" and sell to "+hmm[5]+" / "+time.strftime("%H:%M:%S"))
					if hmm[4]=="polo":
						buy("BTC_ETH",str(hmm[2]),str(hmm[1]))
						trade("eth_btc","SELL",str(hmm[3]),str(hmm[1]))
					else:
						sell("BTC_ETH",str(hmm[3]),str(hmm[1]))
						trade("eth_btc","BUY",str(hmm[2]),str(hmm[1]))
					F = open("mone.txt","a") 
					F.write("Benefice: "+str(hmm[0])+" /volume bought "+str(hmm[1])+" /ask price "+str(hmm[2])+" /bid price "+str(hmm[3])+" /buy from: "+hmm[4]+" and sell to "+hmm[5]+" / "+time.strftime("%H:%M:%S")+" \n")
					F.close()
					break
			else:	
				nigel = volumeboughtt*(hmm[3]-hmm[2])
				if nigel >= 0.002 and volumeboughtt <= 3.18:
					if hmm[4]=="polo":
						buy("BTC_ETH",str(hmm[2]),str(volumeboughtt))
						trade("eth_btc","SELL",str(hmm[3]),str(volumeboughtt))
					else:
						sell("BTC_ETH",str(hmm[3]),str(volumeboughtt))
						trade("eth_btc","BUY",str(hmm[2]),str(volumeboughtt))	
					print("Benefice: "+str(hmm[0])+" /volume bought "+str(hmm[1])+" /ask price "+str(hmm[2])+" /bid price "+str(hmm[3])+" /buy from: "+hmm[4]+" and sell to "+hmm[5]+" / "+time.strftime("%H:%M:%S"))
					print("If I pay 50 euros this be the benifice m8: "+str(nigel))
					
					F = open("mone.txt","a") 
					F.write("Benefice: "+str(hmm[0])+" /volume bought "+str(hmm[1])+" /ask price "+str(hmm[2])+" /bid price "+str(hmm[3])+" /buy from: "+hmm[4]+" and sell to "+hmm[5]+" / "+time.strftime("%H:%M:%S")+" If I pay 50 euros this be the benifice m8: "+str(nigel)+" \n")
					F.close()
					break
				
	print(time.strftime("%H:%M:%S"))
	time.sleep(4)








