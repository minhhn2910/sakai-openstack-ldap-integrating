import ldap
import ldap.modlist as modlist
import json
from role_service import *
default_role = '_member_'
#define base_dn for tenant, user and role; bewlow are just samples
tenant_base_dn='ou=Tenants,dc=cse,dc=hcmut'
user_base_dn= 'ou=Users,dc=cse,dc=hcmut'
role_base_dn='ou=Roles,dc=cse,dc=hcmut'

def build_tenant_entry(tenant_name):
	entry_dn = "cn=%s,%s" %(tenant_name,tenant_base_dn)
	print entry_dn
	attrs = {}
	attrs['objectclass'] = ['groupOfNames']
	attrs['cn'] = '%s'%tenant_name
	#add an cn to not violate the rule of groupOfNames object in LDAP:
	#	Member must not be None
	#in this case, add any abitrary cn to member attrs is OK
	attrs['member'] = "cn=%s,%s" %(default_role,role_base_dn)
	return entry_dn, attrs 

def add_tenant(tenant_name):
	if existed_tenant(tenant_name):
		return False
	tenant_dn,attributes = build_tenant_entry(tenant_name)
	# Open a connection
	l = ldap.initialize("ldap://localhost/")
	# Bind/authenticate with a user with apropriate rights to add objects
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Convert our dict to nice syntax for the add-function using modlist-module
	ldif = modlist.addModlist(attributes)
	l.add_s(tenant_dn,ldif)
	l.unbind_s()  
	# add default admin group to new tenant
	admin_users=['admin','glance','nova'];
	add_users_to_tenant(tenant_name, admin_users, 'admin')
	return True

###user_list = list() type in python
def add_users_to_tenant(tenant, user_list, role=default_role):
	if existed_role_in_tenant(tenant, role):
		return False
	#calling this function must be ensured that role isn't existed in the given tenant
	#need to check outside in the caller method, sync_api.py
	role_dn,attributes = build_role_child_entry(role,tenant)
	# Open a connection
	l = ldap.initialize("ldap://localhost/")
	# Bind/authenticate with a user with apropriate rights to add objects
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Convert our dict to nice syntax for the add-function using modlist-module
	ldif = modlist.addModlist(attributes)
	#ldap.modlist.modifyModlist()
	l.add_s(role_dn,ldif)
	
	users = list()
	for user in user_list:
		users.append("cn=%s,%s" %(user,user_base_dn))
		
	current_tenant_dn='cn=%s,cn=%s,%s'%(role,tenant,tenant_base_dn)

	#add bulk of users to roleOccupant
	old = {'roleOccupant':''}
	new = {'roleOccupant':tuple(users)}

	# Convert place-holders for modify-operation using modlist-module
	ldif = modlist.modifyModlist(old,new)
	# Do the actual modification 
	l.modify_s(current_tenant_dn,ldif)
	# Its nice to the server to disconnect and free resources when done
	l.unbind_s()
	return True
	
def remove_tenant_dn(tenant):
	l = ldap.initialize("ldap://localhost/")
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")	
	deleteDN = "cn=%s,%s" %(tenant,tenant_base_dn)
	#search for child entries first
	baseDN = deleteDN
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = None 
	searchFilter = '(objectClass=*)'
	child_entries = list()
	try:
		ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = l.result(ldap_result_id, 0)
			if (result_data == []):
				break
			else:	
				child_entries.append( result_data[0][0])
	except ldap.LDAPError, e:
		print e

	for entry in child_entries:
		try:
			l.delete_s(entry)
		except ldap.LDAPError, e:
			pass		
			
#now remove tenant entry 
	try:
		l.delete_s(deleteDN)
	except ldap.LDAPError, e:
		pass
	l.unbind_s()

def get_old_tenant_member(tenant,role):
	try:
		l = ldap.open("localhost")
		l.protocol_version = ldap.VERSION3	
	except ldap.LDAPError, e:
		print e
	baseDN = tenant_base_dn
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = ["roleOccupant"]
	searchFilter = "cn=%s"%role
	try:
		ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = l.result(ldap_result_id, 0)
			if (result_data == []):
				break
			else:	
				return result_data[0][1]['roleOccupant']
	except ldap.LDAPError, e:
		print e

def existed_tenant(tenant_name):
	try:
		l = ldap.open("localhost")
		l.protocol_version = ldap.VERSION3	
	except ldap.LDAPError, e:
		print e
	baseDN = tenant_base_dn
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = None
	searchFilter = "cn=%s"%tenant_name
	try:
		ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = l.result(ldap_result_id, 0)
			if (result_data == []):
				return False
			else:	
				return True
	except ldap.LDAPError, e:
		print e

		
	
