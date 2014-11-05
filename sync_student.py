#! /usr/bin/env python
import sys
from ldap_services.sync_api import sync_user
if (len(sys.argv) == 2):
	print 'sync student %s'%sys.argv[1]
	sync_user(sys.argv[1])
	
if (len(sys.argv) == 3):
	print 'sync student %s with password'%sys.argv[1]
	sync_user(sys.argv[1],sys.argv[2])
