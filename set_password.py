#! /usr/bin/env python
import sys
from ldap_services.sync_api import set_user_password
if (len(sys.argv) == 3):
	print 'set password for student %s'%sys.argv[1]
	set_user_password(sys.argv[1],sys.argv[2])
