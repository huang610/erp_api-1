import redis

class MyRedis():
	def __init__(self,host,port):
		try:
			self.r=redis.Redis(host=host,port=port)
		except Exception as e:
			print('redis连接失败！%s'%e)

	def str_set(self,k,v):
		self.r.set(k,v)

	def str_get(self,k):
		res = self.r.get(k)
		if res:
			return res.decode()
		else:
			return None

	def str_delete(self,k):
		'''
		str类型的删除key
		:param k:
		:return:
		'''
		if self.r.get(k):
			self.r.delete(k)
		else:
			return None

	def hash_get(self,k1,k2):
		'''
		hash类型通过大key和小key来获取单个key的值
		:param k1:
		:param k2:
		:return:
		'''
		res = self.r.hget(k1,k2)
		if res:
			return res.decode()
		return None

	def hash_set(self,k1,k2,v):
		'''
		hash类型set
		:param k1:
		:param k2:
		:param v:
		:return:
		'''
		self.r.hset(k1,k2,v)

	def hash_getall(self,k):
		'''
		hash类型获取key里面的所有数据
		通过大key来获取所有的小key和对应value的值,放到一个字典里
		循环字典，将key和value都由bytes类型decode下
		:param k:
		:return:
		'''
		res = self.r.hgetall(k)
		new_res={}
		for k ,v in res.items():
			new_res[k.decode()]=v.decode()
		return new_res

	def hash_del(self,k1,k2):
		'''
		删除某个hash里面小key
		:param k1:
		:param k2:
		:return:
		'''
		self.r.hdel(k1,k2)

	def clean_redis(self):
		'''
		清理redis
		:return:
		'''
		res = self.r.keys()
		if res:
			for key in res:
				self.r.delete(key)
		else:
			return None

# YY=MyRedis('118.24.3.40','HK139bc&*',6379,8)
# print(YY.clean_redis())
# print(YY.hash_getall('ytt_INFO'))




my_redis = MyRedis('192.168.1.140',6379)