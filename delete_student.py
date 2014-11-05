#! /usr/bin/env python
import sys
from ldap_services.sync_api import delete_user
if (len(sys.argv) == 2):
	print 'deleting student %s'%sys.argv[1]
	delete_user(sys.argv[1])
