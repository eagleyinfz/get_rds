'''
Created by auto_sdk on 2015.06.23
'''
from aliyun.api.base import RestApi
class Ram20140214GetUserPolicyRequest(RestApi):
	def __init__(self,domain='ram.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AccountSpace = None
		self.PolicyName = None
		self.UserName = None

	def getapiname(self):
		return 'ram.aliyuncs.com.GetUserPolicy.2014-02-14'
