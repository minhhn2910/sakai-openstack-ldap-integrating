import ldap
import ldap.modlist as modlist
import json
default_role = '_member_'
#define base_dn for tenant, user and role; bewlow are just samples
tenant_base_dn='ou=Tenants,dc=cse,dc=hcmut'
user_base_dn= 'ou=Users,dc=cse,dc=hcmut'
role_base_dn='ou=Roles,dc=cse,dc=hcmut'

def build_role_entry(role_name):
	entry_dn = "cn=%s,%s" %(role_name,role_base_dn)
	print entry_dn
	attrs = {}
	attrs['objectclass'] = ['organizationalRole']
	attrs['cn'] = '%s'%role_name
	return entry_dn, attrs 

def build_role_child_entry(role_name,tenant_name):
	entry_dn = "cn=%s,cn=%s,%s" %(role_name,tenant_name,tenant_base_dn)
	print entry_dn
	attrs = {}
	attrs['objectclass'] = ['organizationalRole']
	attrs['cn'] = '%s'%role_name
	return entry_dn, attrs 	

def add_role(role_name):
	role_dn,attributes = build_role_entry(role_name)
	# Open a connection
	l = ldap.initialize("ldap://localhost/")
	# Bind/authenticate with a user with apropriate rights to add objects
	l.simple_bind_s("cn=Manager,dc=cse,dc=hcmut","openstack")
	# Convert our dict to nice syntax for the add-function using modlist-module
	ldif = modlist.addModlist(attributes)
	l.add_s(role_dn,ldif)
	l.unbind_s()  

	
#there are two positions in the directory service that we need to add role cn
# 1st : the role_base_dn
# 2nd : as a child of tenants
def existed_role_in_tenant(tenant_name, role_name):
	try:
		l = ldap.open("localhost")
		l.protocol_version = ldap.VERSION3	
	except ldap.LDAPError, e:
		print e
	baseDN = "cn=%s,%s"%(tenant_name,tenant_base_dn)
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = None
	searchFilter = "cn=%s"%role_name
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
			
def existed_role(role_name):
	try:
		l = ldap.open("localhost")
		l.protocol_version = ldap.VERSION3	
	except ldap.LDAPError, e:
		print e
	baseDN = role_base_dn
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = None
	searchFilter = "cn=%s"%role_name
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

