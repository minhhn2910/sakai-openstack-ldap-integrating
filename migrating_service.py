#!/usr/bin/python
from ldap_services.sync_api import *
from MySQLdb import *
from collections import namedtuple
import json
import sys
User = namedtuple("User", "user_id eid email name type password")

class DAO(object):
	def __init__(self):
		print 'Initialize DAO object for SAKAI USER'
       
	def fetch_sakai_student(self):
		db = connect("localhost", "root", "nguyen-loc", "sakai")
		cursor = db.cursor() 
		cursor.execute("SELECT * from SAKAI_USER")
		print 'Fetch all '+str(cursor.rowcount)+ ' users from SAKAI_USER table'
		table = cursor.fetchall()
		UserList=list() 
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
#function fetch_courses
#input: none
#output: Courses list, each cource contain student belong to that course
	def fetch_courses(self):
		db = connect("localhost", "root", "nguyen-loc", "sakai")
		cursor = db.cursor() 
		cursor.execute("SELECT * FROM  `SAKAI_SITE`  WHERE  `TYPE`='course'")
		#get all courses from sakai
		print 'Fetch all '+str(cursor.rowcount)+ ' courses from SAKAI_SITE table'
		table = cursor.fetchall()
		CourseList=list() 
		CourseUserList = list()
		for row in table:
			try:
				CourseList.append(row[1])
				cursor.execute("SELECT * FROM  `SAKAI_SITE_USER` WHERE  `SITE_ID` =  '%s' " %row[0])
				user_table = cursor.fetchall()
				UserList = list()
				for user_id_row in user_table:
					#get user_id
					user_id = user_id_row[1]
					cursor.execute("SELECT * FROM  `SAKAI_USER_ID_MAP` WHERE  `USER_ID` =  '%s' " %user_id)
					eid = cursor.fetchone()[1]
					UserList.append(eid)           

				CourseUserList.append(UserList)        
			except (RuntimeError, TypeError, NameError):
				pass
		
		db.close()
		return CourseList, CourseUserList	

	def sync_students(self,user_list):
		for user in user_list:
			#print user[1]
			sync_user(user[1])
	def sync_courses(self,CourseList, CourseUserList):
		for i in range(len(CourseList)):
			print 'Updating '+CourseList[i]
			sync_course(CourseList[i],CourseUserList[i])
	
def main(argv):
	dao = DAO()
	CourseList, CourseUserList = dao.fetch_courses()
	user_list = dao.fetch_sakai_student()
	if len(argv)==0 or len(argv)==2:
		dao.sync_students(user_list)
		dao.sync_courses(CourseList, CourseUserList)
	else:
		if argv[0] == 'student' :
			dao.sync_students(user_list)
		if argv[0] == 'course':
			dao.sync_courses(CourseList, CourseUserList)
		
	#~ dao = DAO()
	#~ CourseList, CourseUserList = dao.fetch_courses()
	#~ dao.sync_course(CourseList, CourseUserList)
	#~ user_list = dao.fetch_sakai_user() 
	#~ dao.sync_ldap(user_list)	
	
	
if __name__ == "__main__":
   main(sys.argv[1:])		

