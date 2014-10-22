import ldap
import ldap.modlist as modlist
import json
#default password : SSHA('stack') 
default_password = '{SSHA}U1jusJV/oMbuKspUOXnRlnFIjE9CAU5A' 
default_role = '_member_'
default_tenant = 'service'
tenant_base_dn='ou=Tenants,dc=cse,dc=hcmut'
user_base_dn= 'ou=Users,dc=cse,dc=hcmut'
role_base_dn='ou=Roles,dc=cse,dc=hcmut'

def build_user_entry(user_name):
	entry_dn = "cn=%s,%s" %(user_name,user_base_dn)
	print entry_dn
	attrs = {}
	attrs['objectclass'] = ['inetOrgPerson']
	attrs['cn'] = '%s'%user_name
	attrs['sn'] = '%s'%user_name
	attrs['userpassword'] = default_password
	return entry_dn, attrs 

def add_user_to_existing_role_occupants(user,roleOccupant):
	l = list()
	l.append(user)
	for x in roleOccupant:
		l.append(x)
	return tuple(l)

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

def add_user(user_dn, attributes):
	# Open a connection
	l = ldap.initialize("ldap://localhost/")
	# Bind/authenticate with a user with apropriate rights to add objects
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Convert our dict to nice syntax for the add-function using modlist-module
	ldif = modlist.addModlist(attributes)
	l.add_s(user_dn,ldif)
	l.unbind_s()  

def add_tenant_user(user_dn, tenant, role, old_tenant_users):
	tenant_dn='cn=%s,cn=%s,%s'%(role,tenant,tenant_base_dn)
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
	
def sync_user(user,tenant=default_tenant,role=default_role,password=default_password):
	if existed_user(user) is True:
		return False
	user_dn, attributes = build_user_entry(user)
	add_user(user_dn,attributes) 
	#add user to project (map to role and tenant for openstack services)
	role_occupants = get_old_tenant_member(tenant,role)
	add_tenant_user(user_dn, tenant, role , role_occupants)	
	return True
	
#sync_user("student2")
#user_dn, attributes = build_user_entry('test1')
#role_occupants = get_old_tenant_member(default_tenant,default_role)
#add_user_to_existing_role_occupants(user_dn,role_occupants)
#add_tenant_user(user_dn, default_tenant, default_role , role_occupants)
#add_user(user_dn,attributes)             
