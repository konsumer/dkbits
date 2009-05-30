#!/usr/bin/python

# handle mail links in browser

BROWSER='sensible-browser'
MAIL_PROVIDER='gmail'

import sys
import urllib
import subprocess

# simplified, multiple values overwrite each other
def urldecode(query):
   d = {}
   a = query.split('&')
   for s in a:
      if s.find('='):
         k,v = map(urllib.unquote, s.split('='))
         d[k] = v
   return d

# mailto:email@domain.com?subject=whatever&whatever=cool

email, raw_fields=" ".join(sys.argv[1:]).split('?')
email=email.split('mailto:')[1]
raw_fields=urldecode(raw_fields)
raw_fields['to']=email

fields={}
for f in raw_fields:
	fields[f.lower()]=raw_fields[f]

if MAIL_PROVIDER == 'gmail' or MAIL_PROVIDER == 'google':
	translate = {
		'subject' : 'su',
	}
	
	link = 'http://mail.google.com/mail/?view=cm&fs=1&tf=1&'


for field in fields:
	try:
		fields[translate[field]] = fields[field]
		del fields[field]
	except KeyError:
		pass


link += urllib.urlencode(fields)

p = subprocess.Popen([BROWSER, link])

