#! /usr/bin/env python
import sys
from ldap_services.sync_api import set_user_password
if (len(sys.argv) == 2):
	f = open('/tmp/user_edit', 'r')
	student = f.read().rstrip()
	print 'set password for student %s'%student
	set_user_password(student,sys.argv[1])
