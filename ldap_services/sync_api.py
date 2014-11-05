from tenant_service import *
from user_service import *
from password_service import *
default_password = 'openstack' 
default_role = '_member_'
default_tenant = 'service'

##############################tenant api#############################
def sync_course(course,user_list,role=default_role):
	if existed_tenant(course) is False:
		print 'newly added course %s'%course
		add_tenant(course)
	if add_users_to_tenant(course, user_list, role) is False:
		#existed role in tenant, add one by one:
		print 'course %s already existed'%course
		print 'adding users to %s with role: %s'%(course,role)
		try:
			for user in user_list:
				old_tenant_users =  get_old_tenant_member(course,role)
				print old_tenant_users
				add_user_to_tenant (user, course, role, old_tenant_users)
		except:
			print 'failed to complete request'
			pass
	return True
	
###############################user api##############################
def sync_user(user,password=default_password):
	try:
		if existed_user(user) is True:
			return False
		user_dn, attributes = build_user_entry(user,makeSecret(password))
		add_user(user_dn,attributes) 
	except:
		pass
	return True
##temporary pass all excepts. Just check the LDAP tree for result
def delete_course(course_name):
	try:
		remove_tenant_dn(course_name)
	except:
		pass
		
def delete_user(user):
	try:
		remove_user_dn(user)
	except:
		pass
	
def set_user_password(user,password):
	try:
		modify_password(user,makeSecret(password))
	except:
		pass

#sync_course('Operating System',['7777','123','8888'])
#delete_course('test_course')
