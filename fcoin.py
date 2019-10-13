# -*- coding:utf-8 -*-
import hashlib,requests
import time
from datetime import datetime
import urllib,hmac,base64
import json

class fcoin(object):
	def __init__(self,public_key,private_key):
		self.public_key = public_key
		self.private_key = private_key
		self.uri='https://api.fcoin.com/v2/'

	# send requests
	def request(self,rtype,method,params):
		array=[]
		for key,value in params.items():
			array.append("{}={}".format(key,value))
		array.sort()
		sign_str="&".join(array)
		
		timestamp=str(int(time.time()*1000))
		full_url=self.uri+method
		if rtype=='GET':
			if sign_str:
				full_url+='?'+sign_str
			sign_str=rtype+full_url+timestamp
		else:
			sign_str=rtype+full_url+timestamp+sign_str
		sign=self.signature(sign_str)
		headers={'FC-ACCESS-KEY':self.public_key,
			 'FC-ACCESS-SIGNATURE':sign,
			 'FC-ACCESS-TIMESTAMP':timestamp}
		r=requests.request(rtype,full_url,headers=headers,json=params)
		result = json.loads(r.text)
		# print('result:'+str(result))
		return result

	# create signature
	def signature(self,sig_str):
		sig_str = base64.b64encode(bytes(sig_str,'utf-8'))
		sign = base64.b64encode(hmac.new(bytes(self.private_key,'utf-8'), sig_str, digestmod=hashlib.sha1).digest())
		return sign

	# get balance
	def balance(self,coin=''):
		data=self.request('GET','accounts/balance',{})
		if data['status']==0:
			newdata={}
			newdata['msg']='Suceess'
			newdata['data']={}
			for row in data['data']:
				newdata['data'][row['currency']+'_balance']=float(row['available'])
				newdata['data'][row['currency']+'_lock']=float(row['frozen'])
			return newdata
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
			return data

	# get balance
	def wallet(self):
		data=self.request('GET','assets/accounts/balance',{})
		if data['status']==0:
			newdata={}
			newdata['msg']='Suceess'
			newdata['data']={}
			for row in data['data']:
				newdata['data'][row['currency']+'_balance']=float(row['available'])
				newdata['data'][row['currency']+'_lock']=float(row['frozen'])
			return newdata
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
			return data

	# get trust_add
	def trust_add(self,coin,direction,price,amount):	#coin=btc_usdt
		params={}
		params['symbol']=coin.replace('_','')
		params['side']=direction
		params['type']='limit'
		params['price']=str(price)
		params['amount']=amount
		data=self.request('POST','orders',params)
		if data['status']==0:
			data['msg']='Suceess'
			id=data['data']
			data['data']={}
			data['data']['id']=id
			data['data']['price']=float(price)
		else:
			data['message'] = data['msg']
			data['msg']='Fail'
		return data

	# get trust_list
	def trust_list(self,coin):				#coin=btc_usdt
		params={}
		params['symbol']=coin.replace('_','')
		params['states']='submitted,partial_filled'
		data=self.request('GET','orders',params)
		if data['status']==0:
			data['msg']='Suceess'
			for row in data['data']:
				row['time']=datetime.fromtimestamp(int(row.pop('created_at')/1000))
				row['price']=float(row['price'])
				row['type']=row.pop('side')
				row['amount_total']=float(row.pop('amount'))
				row['amount_remain']=row['amount_total']-float(row['filled_amount'])
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
		return data

	# get trust_view
	def trust_view(self,coin,id):
		params={}
		params['symbol']=coin.replace('_','')
		data=self.request('GET','orders/%s'%id,params)
		if data['status']==0:
			data['msg']='Suceess'
			data['data']['amount_total']=float(data['data'].pop('amount'))
			data['data']['amount_deal']=float(data['data'].pop('filled_amount'))
			data['data']['amount_remain']=float(data['data']['amount_total'])-float(data['data']['amount_deal'])
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
		return data

	# get trust_cancel
	def trust_cancel(self,coin,id):
		params={}
		params['symbol']=coin.replace('_','')
		data=self.request('POST','orders/%s/submit-cancel'%id,params)
		if data['status']==0:
			data['msg']='Suceess'
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
		return data

	# get trust_list
	def trust_alllist(self,coin,after='',before=''):	#coin=btc_usdt
		params={}
		params['symbol']=coin.replace('_','')
		params['states']='partial_canceled,filled,partial_filled'
		params['limit']=100
		if len(after)>0:
			params['after'] = after
		if len(before) > 0:
			params['before'] = before
		data=self.request('GET','orders',params)
		if data['status']==0:
			data['msg']='Suceess'
			for row in data['data']:
				row['time']=str(datetime.fromtimestamp(int(row['created_at']/1000)))
				row['type']=row.pop('side')
				row['amount_total']=float(row.pop('amount'))
				row['amount_deal']=float(row.pop('filled_amount'))
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
		data['desc']='只返回最新的100条成交记录'
		return data

	# get transfer
	def transfer(self,coin,amount,_type='assets2spot'):
		params={}
		params['currency']=coin
		params['amount']=amount
		if _type=='assets2spot':
			data=self.request('POST','assets/accounts/assets-to-spot',params)
		else:
			data=self.request('POST','assets/accounts/spot-to-assets',params)
		if data['status']==0:
			data['msg']='Suceess'
		else:
			data['message'] = data['msg']
			data['msg'] = 'Fail'
		return data

# print (fcoin().balance())
# print (fcoin().wallet())
# print (fcoin().trust_add('mdt_eth','buy',0.000066,6000))
# print (fcoin().trust_list('mdt_eth'))
# print (fcoin().trust_view('eth_usdt','jlg6BbJAr0cktyH4zjB-GoqisQiVM70='))
# print (fcoin().trust_cancel('mdt_eth','vKssjrjP563cQp85Y4HI1uD-Q0fo6jV6xs3g=='))
# print (fcoin().trust_alllist('eth_usdt'))
# print (fcoin().transfer('btc',0.01))
