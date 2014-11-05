#! /usr/bin/env python
import sys
from ldap_services.sync_api import delete_course
if (len(sys.argv) == 2):
	print 'deleting course %s'%sys.argv[1]
	delete_course(sys.argv[1])
	


