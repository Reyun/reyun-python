#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.2'
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

	def _http_call(self,method):
		postdata = {}
		postdata['appid'] = self._appid
		postdata['when'] = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
		postdata['who'] = self.profile.get('who',_UNKNOWN_)
		postdata['what'] = self.profile.get('what',method)
		postdata['where'] = self.profile.get('what',method)

		self.profile['tz'] = '+8'
		self.profile = dict((key,str(value)) for key, value in self.profile.iteritems() if key not in postdata.keys())

		postdata['context'] = chr(2).join([chr(1).join(x) for x in self.profile.items()])

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

		self.profile = {'tz':tz,'devicetype':devicetype,'deviceid':deviceid, \
					'channelid':channelid,'op':op,'network':network,\
					'os':os,'resolution':resolution}

	def install(self,channelid=_UNKNOWN_):
		"""软件安装报送接口。

		Args:
			channelid:渠道编号. 
		"""		
		self.profile['channelid'] = channelid
		self._http_call('install')

	def reged(self,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,gender='o'):
		"""用户注册账户报送接口。

		Args:
			who:用户ID.
			serverid:服务器编号. 
			channelid:渠道编号.
			gender:f 代表女，m 代表男，o 代表其它.			
		"""		
		self.profile['who'] = who
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid
		self._http_call('reged')

	def startup(self,channelid=_UNKNOWN_):
		"""用户启动软件报送接口。

		Args:
			channelid:渠道编号.
		"""	
		self.profile['channelid'] = channelid
		self._http_call('startup')


	def loggedin(self,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level=_UNKNOWN_,\
				birthday=_UNKNOWN_,gender='o'):
		"""用户登陆报送接口。

		Args:
			who:用户ID.
			serverid:服务器编号. 			
			channelid:渠道编号.
			level:用户等级.
			birthday:2013-10-10.
			gender:f 代表女，m 代表男，o 代表其它.
		"""		
		self.profile['who'] = who
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid
		self.profile['level'] = level
		self.profile['birthday'] = birthday
		self.profile['gender'] = gender
		self._http_call('loggedin')

	def heartbeat(self,who,serverid=_UNKNOWN_,channelid=_UNKNOWN_):
		"""用户心跳报送接口。

		Args:
			who:用户ID.
			serverid:服务器编号. 		
			channelid:渠道编号.				
		"""				
		self.profile['who'] = who
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid		
		self._http_call('hb')

	def session(self,who,sst,set,stt,serverid=_UNKNOWN_,channelid=_UNKNOWN_,):
		"""用户游戏时常报送接口。

		Args:
			who:用户ID.
			sst:开始时间，格式2013-10-10 15:43:22
			set:结束时间，格式2013-10-10 16:22:01
			stt:持续时常(xset-sst)单位秒			
			serverid:服务器编号. 	
			channelid:渠道编号.							
		"""	
		self.profile['who'] = who
		self.profile['sst'] = sst
		self.profile['set'] = set
		self.profile['stt'] = stt		
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid		
		self._http_call('session')

	def event(self,who,what,serverid=_UNKNOWN_,channelid=_UNKNOWN_,extra={}):
		"""自定义事件/多维分析报送接口。
		Args:
			who:用户ID.
			what:事件名称. 
			serverid:服务器编号. 				
			channelid:渠道编号.
			extra:自定义事件属性
		"""				
		self.profile = {}
		self.profile['who'] = who
		self.profile['what'] = what
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid
		self.profile.update(extra.items())
		self._http_call('event')

	def payment(self,who,amount,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level='-1',birthday=_UNKNOWN_,\
				gender='o'):
		"""用户充值报送接口。
		Args:
			who:用户ID.
			serverid:服务器编号. 				
			channelid:渠道编号.
			level:用户等级.
			birthday:2013-10-10.
			gender:f 代表女，m 代表男，o 代表其它.
			amount:用户成功充值，充值的金额
		"""					
		self.profile['who'] = who
		self.profile['amount'] = amount		
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid		
		self.profile['level'] = level
		self.profile['birthday'] = birthday
		self.profile['gender'] = gender	
		self._http_call('payment')

	def economy(self,who,name,num,totalprice,type,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level='-1'):
		"""经济相关报送接口。
		Args:
			who:用户ID.
			name:用户虚拟交易对象的名称.			
			num:用户在此次虚拟交易中的，交易的物品的数量.
			totalprice:用户此次虚拟交易过程中的交易额.	
			type:用户此次虚拟交易的类型,系统产出:SP 购买获得:BP 消费:C .		
			serverid:服务器编号. 				
			channelid:渠道编号.
			level:用户等级.
		"""		
		self.profile['who'] = who
		self.profile['name'] = name	
		self.profile['num'] = num
		self.profile['totalprice'] = totalprice	
		self.profile['type'] = type		
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid	
		self.profile['level'] = level
		self._http_call('economy')

	'''
		
	'''
	def task(self,who,id,state,type,serverid=_UNKNOWN_,channelid=_UNKNOWN_,level='-1'):
		"""任务相关报送接口。
		Args:
			who:用户ID.
			id:任务的id.
			state:任务状态，接受:a； 完成:c
			type:任务类型.main：主线任务，new:主线，sub支线
			serverid:服务器编号.
			channelid:渠道编号.
			level:用户等级.
		"""	
		self.profile['who'] = who
		self.profile['id'] = id
		self.profile['state'] = state	
		self.profile['type'] = type		
		self.profile['serverid'] = serverid
		self.profile['channelid'] = channelid		
		self.profile['level'] = level
		self._http_call('task')					


if __name__=='__main__':
	who = 'Sylar'
	serverid = '测试一服'
	channelid = 'appstore'
	api = API("appkey")

	#设置设备基础
	api.profile(tz='+8',devicetype='Galaxy Nexus',deviceid='123123', \
					op='cmcc',network='WIFI',\
					os='android 4.4',resolution='480*320')
	
	api.install(channelid=channelid)
	api.startup(channelid=channelid)
	api.reged(who,serverid=serverid,channelid=channelid)
	api.loggedin(who,serverid=serverid,channelid=channelid)
	api.heartbeat(who,serverid=serverid,channelid=channelid)
	api.session(who,sst='2013-10-10 15:43:22',set='2013-10-10 16:22:01',stt=1024,serverid=serverid,channelid=channelid)	
	api.event(who,serverid=serverid,channelid=channelid,what='test',extra={'level':99,'drop':10})
	api.payment(who,serverid=serverid,channelid=channelid,amount=10,level=2,gender='m',birthday='2001-10-10')
	api.economy(who,serverid=serverid,channelid=channelid,level=3,num=10,name="xxx",totalprice=1000,type='bp')
	api.task(who,serverid=serverid,channelid=channelid,level=3,id="xxx",state='a',type='1')


