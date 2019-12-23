import requests
class cookies:
	def __init__(self):
		return
	def str2dic(self,cookies_str):
		ret_cookies_dic={}
		if "Cookie: " in cookies_str:
			cookies_str=cookies_str[8:].strip('\n')
		cookies_str=cookies_str.replace(' ','')
		for line in cookies_str.split(';'):
			key,value=line.split('=',1)
			ret_cookies_dic[key]=value
		return ret_cookies_dic

	def dic2str(self,cookies_dic):
		keys_list=cookies_dic.keys()
		values_list=cookies_dic.values()
		ret_cookies_str=''
		for i in range(len(keys_list)):
			ret_cookies_str+=keys_list[i]+'='+values_list[i]+';'
		ret_cookies_str=ret_cookies_str.rstrip(';')
		return ret_cookies_str


	def dic2jar(self,cookies_dic):
		return requests.utils.cookiejar_from_dict(cookies_dic,cookiejar=None,overwrite=True)

	def jar2dic(self,cookies_jar):
		return requests.utils.dict_from_cookiejar(cookies_jar)

	def str2jar(self,cookies_str):
		return self.dic2jar(self.str2dic(cookies_str))
	def jar2str(self,cookies_jar):
		return self.dic2str(self.jar2dic(cookies_jar))

	def all2jar(self,arg_src):
		if isinstance(arg_src,str):
			return self.str2jar(arg_src)
		elif isinstance(arg_src,dict):
			return self.dic2jar(arg_src)
		else:
			return arg_src


cookies=cookies()
