#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.4'
__author__ = 'Sylar (jiangzhenxing@reyun.com)'
'''
Reyun SDK for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
import logging,time,urllib,urllib2,json
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')  

# _ENDPOINT_ = 'http://log.tai-win.com.tw/receive/rest/'	#taiwan
# _ENDPOINT_ = 'http://log.reyun.com/receive/rest/'			#reyun
_ENDPOINT_ = 'http://127.0.0.1:8080/receive/rest/'
_UNKNOWN_ = 'unknown'

class API(object):
	def __init__(self,appid):
		self._appid=appid

	def _http_call(self,method):
		postdata = {}
		postdata['appid'] = self._appid
		postdata['when'] = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
		postdata['who'] = self._profile.get('who',_UNKNOWN_)
		postdata['what'] = self._profile.get('what',method)
		postdata['where'] = self._profile.get('what',method)

		self._profile = dict((key,str(value)) for key, value in self._profile.iteritems() if key not in postdata.keys())

		postdata['context'] = self._profile
		logging.debug(_ENDPOINT_+method)
		logging.debug(json.dumps(postdata))

		req = urllib2.Request(_ENDPOINT_+method, json.dumps(postdata))		
		req.add_header('Content-Type', 'application/json')
		rsp = urllib2.urlopen(req)


		logging.debug('%s[%s]%s' % (method,rsp.getcode(),rsp.read())) 

	def install(self,deviceid,channelid=_UNKNOWN_,serverid=_UNKNOWN_):
		"""软件安装报送接口。

		Args:
			deviceid:设备唯一编号
			serverid:服务器编号			
			channelid:渠道编号. 

		"""		
		self._profile={}
		self._profile['deviceid'] = deviceid
		self._profile['serverid'] = serverid				
		self._profile['channelid'] = channelid
		self._http_call('install')

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
		self._profile={}
		self._profile['deviceid'] = deviceid		
		self._profile['serverid'] = serverid		
		self._profile['channelid'] = channelid
		self._profile['tz'] = tz
		self._profile['devicetype'] = devicetype
		self._profile['op'] = op
		self._profile['network'] = network
		self._profile['os'] = os
		self._profile['resolution'] = resolution

		self._http_call('startup')

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
		self._profile={}
		self._profile['deviceid'] = deviceid
		self._profile['who'] = who
		self._profile['serverid'] = serverid		
		self._profile['channelid'] = channelid		
		self._profile['accountType'] = accountType
		self._profile['gender'] = gender
		self._profile['age'] = age

		self._http_call('register')



	def loggedin(self,deviceid,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=_UNKNOWN_):
		"""用户登陆报送接口。

		Args:
			deviceid:设备唯一编号
			who:用户ID.
			serverid:服务器编号						
			channelid:渠道编号. 
			level:用户等级.
		"""		
		self._profile={}
		self._profile['deviceid'] = deviceid
		self._profile['who'] = who
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid
		self._profile['level'] = level
		self._http_call('loggedin')


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
		self._profile={}
		self._profile['deviceid'] = deviceid
		self._profile['who'] = who

		self._profile['transactionId'] = transactionId
		self._profile['paymentType'] = paymentType		
		self._profile['currencyType'] = currencyType		
		self._profile['currencyAmount'] = currencyAmount		
		self._profile['virtualCoinAmount'] = virtualCoinAmount
		self._profile['iapName'] = iapName
		self._profile['iapAmount'] = iapAmount

		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid		
		self._profile['level'] = level

		self._http_call('payment')




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
		self._profile={}
		self._profile['deviceid'] = deviceid
		self._profile['who'] = who
		self._profile['itemName'] = itemName	
		self._profile['itemAmount'] = itemAmount
		self._profile['itemTotalPrice'] = itemTotalPrice	
		self._profile['serverid'] = serverid				
		self._profile['channelid'] = channelid	
		self._profile['level'] = level
		self._http_call('economy')



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
		self._profile={}
		self._profile['deviceid'] = deviceid		
		self._profile['who'] = who
		self._profile['questId'] = questId
		self._profile['questStatus'] = questStatus	
		self._profile['questType'] = questType		
		self._profile['serverid'] = serverid		
		self._profile['channelid'] = channelid		
		self._profile['level'] = level
		self._http_call('quest')					

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
		self._profile={}		
		self._profile['deviceid'] = deviceid				
		self._profile['who'] = who
		self._profile['what'] = what
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid				
		self._profile.update(extra.items())
		self._http_call('event')

	def heartbeat(self,deviceid,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1):
		"""用户心跳报送接口。

		Args:
			deviceid:设备唯一编号								
			who:用户ID.
			serverid:服务器编号. 		
			channelid:渠道编号.	
			level:用户等级			
		"""				
		self._profile={}
		self._profile['deviceid'] = deviceid						
		self._profile['who'] = who
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid		
		self._profile['level'] = level
		self._http_call('heartbeat')




if __name__=='__main__':
	who = 'Sylar'
	serverid = '测试一服'
	channelid = 'appstore'
	api = API("appkey")
	
	api.install(deviceid="xxxxx",serverid=serverid,channelid=channelid)
	api.startup(deviceid="xxxxx",serverid=serverid,channelid=channelid,tz="+8",devicetype="ios",\
		op="cmcc",network="3g",os="ios",resolution="400*600")
	api.register(deviceid="xxxxx",who=who,accountType="qq",serverid=serverid,channelid=channelid,gender="f",age=19)
	api.loggedin(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,level=11)
	api.payment(deviceid="xxxxx",who=who,transactionId="0000001",paymentType="IAP",currencyType='CNY',currencyAmount=100,\
				virtualCoinAmount=10000,iapName="keys",iapAmount=1,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=7)
	api.economy(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,level=3,itemAmount=10,itemName="xxx",itemTotalPrice=1000)
	api.quest(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,level=3,questId="xxx",questStatus='a',questType='main')
	api.event(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid,what='test',extra={'deviceid':"xxxxxxx",'level':99,'drop':10})
	api.heartbeat(deviceid="xxxxx",who=who,serverid=serverid,channelid=channelid)


