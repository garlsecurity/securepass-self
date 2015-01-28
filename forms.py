## Forms mate :)
from wtforms import BooleanField, TextField, PasswordField, validators, StringField, TextAreaField
from flask.ext.wtf import Form
from datetime import timedelta


class PasswordChange(Form):

    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Repeat Password')


class SshKey(Form):

    sshkey = TextAreaField('SSH Public Key')
