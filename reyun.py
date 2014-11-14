#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.4'
__author__ = 'Sylar (jiangzhenxing@reyun.com)'
'''
Reyun SDK for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
import logging,time,json
import urllib,urllib2
import threading,Queue
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')  

# _ENDPOINT_ = 'http://log.reyun.com/receive/rest/'			#reyun
_ENDPOINT_ = 'http://192.168.2.25:8080/receive/rest/'
_UNKNOWN_ = 'unknown'
_BUFFER_NAME_ = 'reyun-buffer'
_RETRY_TIMES = 3

def _http_call(appid,method,data):
	postdata = {}
	postdata['appid'] = appid
	postdata['when'] = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
	postdata['who'] = data.get('who',_UNKNOWN_)
	postdata['what'] = data.get('what',method)
	postdata['where'] = data.get('what',method)

	data = dict((key,str(value)) for key, value in data.iteritems() if key not in postdata.keys())

	postdata['context'] = data
	jsondata = json.dumps(postdata)
	logging.debug(_ENDPOINT_+method)
	logging.debug(jsondata)

	req = urllib2.Request(_ENDPOINT_+method, jsondata)		
	req.add_header('Content-Type', 'application/json')
	rsp = None
	try:
		rsp = urllib2.urlopen(req)
	except :
		pass

	status = 1
	content = ''

	if rsp != None :
		content = rsp.readlines()
		status = json.loads(content[0])['status']
		if status != 0:
			logging.error('[args error]    %s    %s' % (jsondata,content))       
	logging.debug('%s[%s]%s' % (method,status,content))       

	return status

class Consumer(threading.Thread): 
	def __init__(self,appid, queue): 
		threading.Thread.__init__(self)
		self._appid = appid
		self._queue = queue 


	def run(self):
		while True: 
			if self._queue:
				msg = self._queue.blpop(_BUFFER_NAME_)[1]
				data =  eval(msg)
				if data['retry'] < _RETRY_TIMES:
					data['retry'] += 1
					status = _http_call(self._appid,data['method'],data['data'])
					if status == 1:
						self._queue.rpush(_BUFFER_NAME_,json.dumps(data))
				else:
					logging.error('[retry 3 times]    %s' % msg)  

class Producer():
	def __init__(self,appid,queue=None):
		self._appid=appid
		self._queue=queue

	def produce(self,method,data):
		del data['self']
		if self._queue:
			self._queue.rpush(_BUFFER_NAME_,{'method':method,'data':data,'retry':0})
		else:
			_http_call(self._appid,method,data)

class API(object):
	def __init__(self,appid,buffer=False,host='localhost',port=6379,db=0):
		self._appid=appid
		self._queue = None
		self.buffer = buffer
		if self.buffer:
			import redis
			self._queue = redis.StrictRedis(host,port,db)
		self._consumer = Consumer(appid,self._queue)
		self._producer = Producer(appid,self._queue)

	def start(self):
		print self.buffer
		if self.buffer:
			self._consumer.start()
		else:
			logging.debug("buffer is not ture,the Consumer buffer will not work")      			
		


	def install(self,deviceid,channelid=_UNKNOWN_,serverid=_UNKNOWN_):
		"""软件安装报送接口。

		Args:
			deviceid:设备唯一编号
			serverid:服务器编号			
			channelid:渠道编号. 

		"""		
		self._producer.produce('install',locals())

	def startup(self,deviceid,serverid=_UNKNOWN_,channelid=_UNKNOWN_,tz="+8",devicetype=_UNKNOWN_,op=_UNKNOWN_\
		,network=_UNKNOWN_,os=_UNKNOWN_,resolution=_UNKNOWN_):
		"""用户启动软件报送接口。

		Args:
			deviceid:设备唯一编号
			serverid:服务器编号			
			channelid:渠道编号. 
			tz:时区
			devicetype:设备类型
			op:运营商.
			network:网络制式2G,3G,WIFI.
			os:操作系统.
			resolution:分辨率.			
		"""	
		self._producer.produce('startup',locals())

	def register(self,deviceid,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,accountType=_UNKNOWN_,\
		gender=_UNKNOWN_,age=-1):
		"""用户注册账户报送接口。

		Args:
			deviceid:设备唯一编号
			who:用户ID.
			serverid:服务器编号						
			channelid:渠道编号. 
			accountType:账户类型.
			gender:f 代表女，m 代表男，o 代表其它.		
			age:年龄	
		"""		
		self._producer.produce('register',locals())



	def loggedin(self,deviceid,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=_UNKNOWN_):
		"""用户登陆报送接口。

		Args:
			deviceid:设备唯一编号
			who:用户ID.
			serverid:服务器编号						
			channelid:渠道编号. 
			level:用户等级.
		"""		
		self._producer.produce('loggedin',locals())


	def payment(self,deviceid,who,transactionId,paymentType,currencyType,currencyAmount,virtualCoinAmount,\
				iapName,iapAmount,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1):
		"""用户充值报送接口。
		Args:
			deviceid:设备唯一编号		
			who:用户ID.
			transactionId:交易的流水号.
			paymentType:支付类型，例如支付宝，银联，苹果、谷歌官方等;
						如果是系统赠送的，paymentType为：FREE.
			currencyType:货币类型，按照国际标准组织ISO 4217中规范的3位字母，例如CNY人民币、USD美金等，
							详情,http://zh.wikipedia.org/wiki/ISO_4217.
			currencyAmount:支付的真实货币的金额.
			virtualCoinAmount:通过充值获得的游戏内货币的数量.
			iapName:游戏内购买道具的名称.
			iapAmount:游戏内购买道具的数量.
			serverid:服务器编号. 							
			channelid:渠道编号.			
			level:用户等级.
		"""				
		self._producer.produce('payment',locals())


	def economy(self,deviceid,who,itemName,itemAmount,itemTotalPrice,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1):
		"""经济相关报送接口。
		Args:
			deviceid:设备唯一编号				
			who:用户ID.
			itemName:用户虚拟交易对象的名称.			
			itemAmount:用户在此次虚拟交易中的，交易的物品的数量.
			itemTotalPrice:用户此次虚拟交易过程中的交易额.	
			serverid:服务器编号. 	
			channelid:渠道编号.									
			level:用户等级.
		"""		
		self._producer.produce('economy',locals())


	def quest(self,deviceid,who,questId,questStatus,questType,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1):
		"""任务相关报送接口。
		Args:
			deviceid:设备唯一编号						
			who:用户ID.
			questId:任务的id.
			questStatus:任务状态，接受:a； 完成:c； 失败:f
			questType:任务类型.main：主线任务，new:主线，sub支线
			serverid:服务器编号.
			channelid:渠道编号.			
			level:用户等级.
		"""	
		self._producer.produce('quest',locals())					

	def event(self,deviceid,who,what,serverid=_UNKNOWN_,channelid=_UNKNOWN_,extra={}):
		"""自定义事件/多维分析报送接口。
		Args:
			deviceid:设备唯一编号								
			who:用户ID.
			what:事件名称. 
			serverid:服务器编号. 										
			channelid:渠道编号.
			extra:自定义事件属性
		"""		
		self._producer.produce('event',locals())

	def heartbeat(self,deviceid,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1):
		"""用户心跳报送接口。

		Args:
			deviceid:设备唯一编号								
			who:用户ID.
			serverid:服务器编号. 		
			channelid:渠道编号.	
			level:用户等级			
		"""				
		self._producer.produce('heartbeat',locals())


if __name__=='__main__':

	who = 'Sylar'
	serverid = '测试一服'
	channelid = 'appstore'


	api = API("appkey",buffer=True,host='x00',port=6379,db=0)
	
	api.install(deviceid="xxxxxx",serverid=serverid,channelid=channelid)

	# api.startup(deviceid="xxxxx",serverid=serverid,channelid=channelid,tz="+8",devicetype="ios",\
	# 	op="cmcc",network="3g",os="ios",resolution="400*600")
	# api.register(deviceid="xxxxx",who=who,accountType="qq",serverid=serverid,channelid=channelid,gender="f",age=19)
	# api.loggedin(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,level=11)
	# api.payment(deviceid="xxxxx",who=who,transactionId="0000001",paymentType="IAP",currencyType='CNY',currencyAmount=100,\
	# 			virtualCoinAmount=10000,iapName="keys",iapAmount=1,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=7)
	# api.economy(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,level=3,itemAmount=10,itemName="xxx",itemTotalPrice=1000)
	# api.quest(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,level=3,questId="xxx",questStatus='a',questType='main')
	# api.event(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,what='test',extra={'deviceid':"xxxxxxx",'level':99,'drop':10})
	# api.heartbeat(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid)
	
	#如果buffer等于True，需要手动启动线程报送线程
	api.start()


