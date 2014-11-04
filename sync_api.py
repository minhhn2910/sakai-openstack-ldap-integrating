from tenant_service import *
from user_service import *
from password_service import *
default_password = 'openstack' 
default_role = '_member_'
default_tenant = 'service'
##############################tenant api#############################
def sync_tenant(tenant,user_list,role=default_role):
	if existed_tenant(tenant) is True:
		
#	user_dn, attributes = build_user_entry(user)
#	add_user(user_dn,attributes) 
	#add user to project (map to role and tenant for openstack services)
#	role_occupants = get_old_tenant_member(tenant,role)
#	add_tenant_user(user_dn, tenant, role , role_occupants)	
	return true
###############################user api##############################
def add_user(user,password=default_password):
	if existed_user(user) is True:
		return False
	user_dn, attributes = build_user_entry(user,makeSecret(password))
	add_user(user_dn,attributes) 
	#add user to project (map to role and tenant for openstack services)
#	role_occupants = get_old_tenant_member(tenant,role)
#	add_user_to_tenant(user_dn, tenant, role , role_occupants)	
	return True
	
def delete_user(user):
	return true
def set_user_password(user,password):
	return true

