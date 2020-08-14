#!/usr/bin/env python

import sys
import site

site.addsitedir('/usr/lib/python2.7/site-packages/')

sys.path.insert(0, '/var/www/hitme')

from app import app as application

