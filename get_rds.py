# -*- coding: utf-8 -*-
'''
Created on 2016-6-28
@author: Jason Le
For security reason, source code keep downloading code in comment status. 
You can remove the comment for the line including "urllib.urlretrieve".

Ϊ��ȫ�����Դ���򲢲��������أ����ֶ�ȡ��ע��: urllib.urlretrieve
'''

import sys,os,shutil,string
import re
import urllib,urllib2
import logging
import time
from  datetime  import timedelta
from  datetime  import datetime
import aliyun.api


# Show the progress of downloading.
def Schedule(a,b,c):
  #a:�Ѿ����ص����ݿ�
  #b:���ݿ�Ĵ�С
  #c:Զ���ļ��Ĵ�С
  percentage = 100.0 * a * b / c
  if percentage > 100 :
    percentage = 100
  #print '%.2f%%' % percentage
  sys.stdout.write('%.2f%%\r' % percentage)


BackUpPath='/export/data/ali-rds/'
aliyun.setDefaultAppInfo("your ACCESSKEYID of rds", "your ACCESSKEYSECRET of rds")

logging.basicConfig(level=logging.INFO,
  format='%(asctime)s %(levelname)s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename=BackUpPath + 'get_rds.log',
  filemode='a')    


#RDSʵ����
my_rdsname = "your instance name"
my_diqu = "cn-beijing" # It should be your location of rds


#��ѯ�����ļ�����Ϣ
#�ӷ���ǰʱ��ǰ��24Сʱ����Ϊһ��RDS���Զ�������1��1��
dnow = datetime.now()
dstart = dnow - timedelta(hours=24)
d1 = dstart.strftime("%Y-%m-%dT%H:%MZ")
d2 = dnow.strftime("%Y-%m-%dT%H:%MZ")
#print d1, d2 #just for debug
ali = aliyun.api.Rds20140815DescribeBackupsRequest()
ali.RegionId = my_diqu
ali.DBInstanceid = my_rdsname
ali.StartTime = d1
ali.EndTime =  d2

#ÿ��ִ��ǰ�����rds.swap�����ݣ��Ա������ű��ж��Ƿ����سɹ����գ���ʾ�ޱ������أ�
swapfile=open(BackUpPath+'rds.swap','w')
swapfile.write("")
swapfile.close

#��ȡ�����б�������ģʽ�£�1���1��ȫ����
try:
  f = ali.getResponse()
  if("Code" in f):
    print("Fasle")
    print(f["Code"])
    print(f["Message"]) 
  else:
    f = ali.getResponse()
    #print(f)
    f = str(f)

    my_re = re.compile(r"(http://.*?)',")
    my_data = my_re.findall(f)
    my_url = my_data

    my_len = len(my_url) 
    print("\n")
    print "From %r to %r, start download, please wait..." % (ali.StartTime, ali.EndTime)
    print("\n")

    for m in my_url:
      if ( re.search(r".internal.",m) ):
        continue

      res = re.findall(r'hins(.*)\?OSSAccessKeyId',m)
      filename= "hins" + res[0]

      # Generating a file recording the real downloaded file name for further desposal, say auto recovery
      # ��Ȼ����Դ���־�ļ�������2�ж������ص��ļ��������ṩһ��rds.swap��¼���ص��ļ��������Ǹ����㣬����ά����
      if( len(filename)!=4 ):
        swapfile=open(BackUpPath+'rds.swap','w')
        swapfile.write(filename)
        swapfile.close

      curr = time.strftime('%Y-%m-%d %H:%M:%S')
      print "[%r] downloading %r, please wait..." % (curr,filename)
      logging.info('Start downloading: %r'% (filename))

      urllib.urlretrieve(m, BackUpPath+filename, Schedule)
      logging.info('Successfully download: %r'% (filename))
      #break

    endtime = time.strftime('%Y-%m-%d %H:%M:%S')
    dend = datetime.now()
    dtotal = dend-dnow
    print "[%r] downloading over, please check dir[%r]!" % (endtime, BackUpPath)
    logging.info('Task over, using : %r seconds' % (dtotal.seconds))

except Exception,e:
  print(e)
