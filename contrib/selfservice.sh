#!/bin/bash
##
## Startup for Docker
## (c) 2015 Giuseppe Paterno' <gpaterno@gpaterno.com>
##

## Create SecurePass configuration file
SP_APP_ID=${SP_APP_ID:-none}
SP_APP_SECRET=${SP_APP_SECRET:-none}

cat  << __EOF__ > /etc/securepass.conf
[default]
APP_ID = $SP_APP_ID
APP_SECRET = $SP_APP_SECRET
__EOF__

echo SecurePass application ID: $SP_APP_ID

## Generate random string for cookies
RAND=$(openssl rand -hex 16)
sed -i -e "s/generate_secret_key/$RAND/" /srv/securepass-self/selfservice.py 

## Load WSGI
uwsgi --ini /srv/securepass-self/contrib/selfservice.ini
