#!/usr/bin/python
from ldap_service import sync_user
from MySQLdb import *
from collections import namedtuple
import json
User = namedtuple("User", "user_id eid email name type password")
class DAO(object):
	def __init__(self):
		print 'Initialize DAO object for SAKAI USER'
       
	def fetch_sakai_user(self):
		db = connect("localhost", "root", "nguyen-loc", "sakai")
		cursor = db.cursor() 
		cursor.execute("SELECT * from SAKAI_USER")
		print 'Fetch all '+str(cursor.rowcount)+ ' users from SAKAI_USER table'
		table = cursor.fetchall()
		UserList=[] 
		for row in table:
			try:
				cursor.execute("SELECT * FROM  `SAKAI_USER_ID_MAP` WHERE  `USER_ID` =  '%s' " %row[0])
				eid = cursor.fetchone()[1]
				user = User(str(row[0]), eid,  str(row[1]), str(row[3]), str(row[5]), str(row[6]))	
				UserList.append(user)             
			except (RuntimeError, TypeError, NameError):
				pass
		db.close()
		return UserList

	def sync_ldap(self,user_list):
		for user in user_list:
			#print user[1]
			sync_user(user[1])
		
dao = DAO()
user_list = dao.fetch_sakai_user() 
dao.sync_ldap(user_list)
