import ldap
import ldap.modlist as modlist
import json

#define base_dn for tenant, user and role; bewlow are just samples
tenant_base_dn='ou=Tenants,dc=cse,dc=hcmut'
user_base_dn= 'ou=Users,dc=cse,dc=hcmut'
role_base_dn='ou=Roles,dc=cse,dc=hcmut'

def build_user_entry(user_name,password):
	entry_dn = "cn=%s,%s" %(user_name,user_base_dn)
	print entry_dn
	attrs = {}
	attrs['objectclass'] = ['inetOrgPerson']
	attrs['cn'] = '%s'%user_name
	attrs['sn'] = '%s'%user_name
	attrs['userpassword'] = password
	return entry_dn, attrs 

def add_user_to_existing_role_occupants(user,roleOccupant):
	l = list()
	l.append(user)
	for x in roleOccupant:
		l.append(x)
	return tuple(l)

def modify_password(user,password):
	old_password = get_old_hashed_password(user)
	user_dn='cn=%s,%s'%(user,user_base_dn)
	print 'change pass ' + user_dn
	l = ldap.initialize("ldap://localhost/")
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Some place-holders for old and new values
	old = {'userpassword':old_password}
	new = {'userpassword':password}

	# Convert place-holders for modify-operation using modlist-module
	ldif = modlist.modifyModlist(old,new)

	# Do the actual modification 
	l.modify_s(user_dn,ldif)

	# Its nice to the server to disconnect and free resources when done
	l.unbind_s()

def remove_user_dn(user):
	l = ldap.initialize("ldap://localhost/")
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")	
	deleteDN = "cn=%s,%s" %(user,user_base_dn)
	try:
		l.delete_s(deleteDN)
	except ldap.LDAPError, e:
		print e
	l.unbind_s()					
	
def get_old_hashed_password(user):
	try:
		l = ldap.open("localhost")
		l.protocol_version = ldap.VERSION3	
	except ldap.LDAPError, e:
		print e
	baseDN = user_base_dn
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = ["userpassword"]
	searchFilter = "cn=%s"%user
	try:
		ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = l.result(ldap_result_id, 0)
			if (result_data == []):
				break
			else:	
				return result_data[0][1]['userPassword'][0]
	except ldap.LDAPError, e:
		print e
	
def add_user(user_dn, attributes):
	# Open a connection
	l = ldap.initialize("ldap://localhost/")
	# Bind/authenticate with a user with apropriate rights to add objects
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Convert our dict to nice syntax for the add-function using modlist-module
	ldif = modlist.addModlist(attributes)
	l.add_s(user_dn,ldif)
	l.unbind_s()  

def add_user_to_tenant(user, tenant, role, old_tenant_users):
	tenant_dn='cn=%s,cn=%s,%s'%(role,tenant,tenant_base_dn)
	user_dn = 'cn=%s,%s'%(user,user_base_dn)
	print tenant_dn
	new_tenant_users = add_user_to_existing_role_occupants(user_dn,old_tenant_users)
	l = ldap.initialize("ldap://localhost/")
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Some place-holders for old and new values
	old = {'roleOccupant':old_tenant_users}
	new = {'roleOccupant':new_tenant_users}

	# Convert place-holders for modify-operation using modlist-module
	ldif = modlist.modifyModlist(old,new)

	# Do the actual modification 
	l.modify_s(tenant_dn,ldif)

	# Its nice to the server to disconnect and free resources when done
	l.unbind_s()

def existed_user(user_name):
	try:
		l = ldap.open("localhost")
		l.protocol_version = ldap.VERSION3	
	except ldap.LDAPError, e:
		print e
	baseDN = user_base_dn
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = None
	searchFilter = "cn=%s"%user_name
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

        
