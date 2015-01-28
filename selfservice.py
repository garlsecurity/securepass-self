import sys, os
from securepass import securepass, utils
from flask import Flask, request, render_template, redirect, session, url_for
from forms import PasswordChange, SshKey
from flask.ext.cas import CAS
import textwrap

app = Flask(__name__)
cas = CAS(app)


@app.route('/')
def user_details():
    user = cas.username

    ## Load config
    config = utils.loadConfig()

    ## Config the handler
    sp_handler = securepass.SecurePass(app_id=config['app_id'],
                                       app_secret=config['app_secret'],
                                       endpoint=config['endpoint'])

    if user is not None:
        try:
            spuser = sp_handler.user_info(user=user)
            session['username'] = user

            xattrs = sp_handler.users_xattr_list(user=user)

            ## need to understand if the xattr is in list
            if 'sshkey' in xattrs:
                sshkey = textwrap.wrap(xattrs['sshkey'], width=80)

            else:
                sshkey = ""

            return render_template('user.html', spuser=spuser, xattrs=xattrs, user=user, sshkey=sshkey)

        except:
            return "Bad thing happened!"

    return redirect('/login/')


@app.route('/password', methods=['GET', 'POST'])
def user_password():

    #if 'username' not in session:
    #        return redirect(url_for('user_details'))
    user = cas.username
    form = PasswordChange(request.form)

    if request.method == 'POST' and form.validate():
        ## Load config
        config = utils.loadConfig()

        ## Config the handler
        sp_handler = securepass.SecurePass(app_id=config['app_id'],
                                           app_secret=config['app_secret'],
                                           endpoint=config['endpoint'])

        ## Change password
        sp_handler.user_password_change(user=user, password=form.password.data)


        return "Password changed"

    return render_template('password_change.html', form=form, user=user)

@app.route('/sshkey', methods=['GET', 'POST'])
def user_ssh():
    user = cas.username
    form = SshKey(request.form)

    if request.method == 'POST' and form.validate():
        ## Load config
        config = utils.loadConfig()

        ## Config the handler
        sp_handler = securepass.SecurePass(app_id=config['app_id'],
                                           app_secret=config['app_secret'],
                                           endpoint=config['endpoint'])

        ## Set ssh key
        ## Need to trap SecurePass errors'
        sp_handler.users_xattr_set(user=user, attribute='sshkey', value=form.sshkey.data)

        return "SSH Key changed"

    return render_template('ssh_change.html', form=form, user=user)


if __name__ == '__main__':
    app.secret_key = 'generate_secret_key'
    app.config['CAS_SERVER'] = 'https://beta.secure-pass.net/'
    app.config['CAS_AFTER_LOGIN'] = 'user_details'
    app.config['CAS_LOGIN_ROUTE'] = '/cas/login'
    app.run()
