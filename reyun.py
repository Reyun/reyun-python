#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.3'
__author__ = 'Sylar (jiangzhenxing@reyun.com)'
'''
Reyun SDK for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
import logging,time,urllib,urllib2
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')  

_ENDPOINT_ = 'http://log.reyun.com/receive/receive'
# _ENDPOINT_ = 'http://192.168.1.141:8642/receive/receive'
_UNKNOWN_ = 'unknown'

class API(object):
	def __init__(self,appid):
		self._appid=appid
		self._profile = {'tz':'+8','devicetype':_UNKNOWN_,'deviceid':_UNKNOWN_, \
					'channelid':_UNKNOWN_,'op':_UNKNOWN_,'network':_UNKNOWN_,\
					'os':_UNKNOWN_,'resolution':_UNKNOWN_}		

	def _http_call(self,method):
		postdata = {}
		postdata['appid'] = self._appid
		postdata['when'] = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
		postdata['who'] = self._profile.get('who',_UNKNOWN_)
		postdata['what'] = self._profile.get('what',method)
		postdata['where'] = self._profile.get('what',method)

		self._profile = dict((key,str(value)) for key, value in self._profile.iteritems() if key not in postdata.keys())

		postdata['context'] = chr(2).join([chr(1).join(x) for x in self._profile.items()])

		req = urllib2.Request(_ENDPOINT_, urllib.urlencode(postdata))
		rsp = urllib2.urlopen(req)

		logging.debug('[%s]%s' % (rsp.getcode(),rsp.read())) 

	def profile(self ,tz=_UNKNOWN_,devicetype=_UNKNOWN_,deviceid=_UNKNOWN_, \
					op=_UNKNOWN_,network=_UNKNOWN_,os=_UNKNOWN_,resolution=_UNKNOWN_):
		"""设备基础属性。

		Args:
			tz:时区.
			devicetype:设备类型.
			deviceid:设备唯一编号. 
			op:运营商.
			network:网络制式2G,3G,WIFI.
			os:操作系统.
			resolution:分辨率.
		"""

		self._profile = {'tz':tz,'devicetype':devicetype,'deviceid':deviceid, \
					'channelid':channelid,'op':op,'network':network,\
					'os':os,'resolution':resolution}

	def install(self,channelid=_UNKNOWN_):
		"""软件安装报送接口。

		Args:
			channelid:渠道编号. 
		"""		
		self._profile['channelid'] = channelid
		self._http_call('install')

	def reged(self,who,accountType=_UNKNOWN_,serverid=_UNKNOWN_,channelid=_UNKNOWN_,gender='o'):
		"""用户注册账户报送接口。

		Args:
			who:用户ID.
			accountType:账户类型.
			serverid:服务器编号. 
			channelid:渠道编号.
			gender:f 代表女，m 代表男，o 代表其它.			
		"""		
		self._profile['who'] = who
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid
		self._http_call('reged')

	def startup(self,channelid=_UNKNOWN_):
		"""用户启动软件报送接口。

		Args:
			channelid:渠道编号.
		"""	
		self._profile['channelid'] = channelid
		self._http_call('startup')


	def loggedin(self,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=_UNKNOWN_,\
				age=-1,gender=_UNKNOWN_):
		"""用户登陆报送接口。

		Args:
			who:用户ID.
			serverid:服务器编号. 			
			channelid:渠道编号.
			level:用户等级.
			age: 年龄.
			gender:f 代表女，m 代表男，o 代表其它.
		"""		
		self._profile['who'] = who
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid
		self._profile['level'] = level
		self._profile['age'] = age
		self._profile['gender'] = gender
		self._http_call('loggedin')

	def heartbeat(self,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_):
		"""用户心跳报送接口。

		Args:
			who:用户ID.
			serverid:服务器编号. 		
			channelid:渠道编号.				
		"""				
		self._profile['who'] = who
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid		
		self._http_call('hb')

	def event(self,who,what,serverid=_UNKNOWN_,channelid=_UNKNOWN_,extra={}):
		"""自定义事件/多维分析报送接口。
		Args:
			who:用户ID.
			what:事件名称. 
			serverid:服务器编号. 				
			channelid:渠道编号.
			extra:自定义事件属性
		"""				
		self._profile = {}
		self._profile['who'] = who
		self._profile['what'] = what
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid
		self._profile.update(extra.items())
		self._http_call('event')

	def payment(self,who,transactionId,paymentType,currencyType,currencyAmount,virtualCoinAmount,\
				iapName,iapAmount,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1,age=-1,gender=_UNKNOWN_):
		"""用户充值报送接口。
		Args:
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
			age:年龄.
			gender:f 代表女，m 代表男，o 代表其它.
		"""					
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
		self._profile['age'] = age
		self._profile['gender'] = gender	
		self._http_call('payment')

	def economy(self,who,itemName,itemAmount,itemTotalPrice,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=-1):
		"""经济相关报送接口。
		Args:
			who:用户ID.
			itemName:用户虚拟交易对象的名称.			
			itemAmount:用户在此次虚拟交易中的，交易的物品的数量.
			itemTotalPrice:用户此次虚拟交易过程中的交易额.	
			serverid:服务器编号. 				
			channelid:渠道编号.
			level:用户等级.
		"""		
		self._profile['who'] = who
		self._profile['itemName'] = itemName	
		self._profile['itemAmount'] = itemAmount
		self._profile['itemTotalPrice'] = itemTotalPrice	
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid	
		self._profile['level'] = level
		self._http_call('economy')

	'''
		
	'''
	def quest(self,who,questId,questStatus,questType,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level='-1'):
		"""任务相关报送接口。
		Args:
			who:用户ID.
			questId:任务的id.
			questStatus:任务状态，接受:a； 完成:c； 失败:f
			questType:任务类型.main：主线任务，new:主线，sub支线
			serverid:服务器编号.
			channelid:渠道编号.
			level:用户等级.
		"""	
		self._profile['who'] = who
		self._profile['questId'] = questId
		self._profile['questStatus'] = questStatus	
		self._profile['questType'] = questType		
		self._profile['serverid'] = serverid
		self._profile['channelid'] = channelid		
		self._profile['level'] = level
		self._http_call('task')					


if __name__=='__main__':
	who = 'Sylar'
	serverid = '测试一服'
	channelid = 'appstore'
	api = API("appkey")
	
	#设置设备基础
	api.profile(tz='+8',devicetype='Galaxy Nexus',deviceid='123123', \
					op='cmcc',network='WIFI',os='android 4.4',resolution='480*320')
	
	api.install(channelid=channelid)
	api.startup(channelid=channelid)
	api.reged(who,accountType="qq",serverid=serverid,channelid=channelid)
	api.loggedin(who,serverid=serverid,channelid=channelid)
	api.heartbeat(who,serverid=serverid,channelid=channelid)
	api.event(who,serverid=serverid,channelid=channelid,what='test',extra={'level':99,'drop':10})
	api.payment(who,transactionId="0000001",paymentType="IAP",currencyType='CNY',currencyAmount=100,\
				virtualCoinAmount=10000,iapName="keys",iapAmount=1,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=7,age=21,gender='o')
	api.economy(who,serverid=serverid,channelid=channelid,level=3,itemAmount=10,itemName="xxx",itemTotalPrice=1000)
	api.quest(who,serverid=serverid,channelid=channelid,level=3,questId="xxx",questStatus='a',questType='main')

