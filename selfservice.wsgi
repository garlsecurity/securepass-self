activate_this = '/srv/securepass-self/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys,os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from selfservice import app as application

application.secret_key = 'generate_secret_key'
application.config['CAS_SERVER'] = 'https://beta.secure-pass.net/'
application.config['CAS_AFTER_LOGIN'] = 'user_details'
application.config['CAS_LOGIN_ROUTE'] = '/cas/login'
