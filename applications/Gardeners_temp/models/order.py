# -*- coding: utf-8 -*-
userauth=Auth(db,controller='order')
from gluon.validators import Validator
class IS_PHONE(Validator):
    def __init__(this,error_message='Must be a valid ph. number'):
        this.error_message=error_message
    def __call__(this,value):
        if value.length==10 and value.isdigit():
            return (value,none)
        return (value,translate(this.error_message))
db.define_table(
    userauth.settings.table_user_name,
    Field('first_name', length=128, default='',requires=IS_NOT_EMPTY(error_message=userauth.messages.is_empty)),
    Field('last_name', length=128, default='',requires=IS_NOT_EMPTY(error_message=userauth.messages.is_empty)),
    Field('username',length=128,default=''),
    Field('email', length=128, default='',unique=True),
    Field('phone_number',length=128,default='',requires=IS_MATCH('^[0-9]{8,16}$',error_message='Must be a valid phone number')),
    Field('password', 'password', length=512, readable=False, label='Password'),
    Field('registration_key', length=512, writable=False, readable=False, default=''),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default=''),
    format='%(first_name)s %(last_name)s')

ouser = db[userauth.settings.table_user_name]
ouser.password.requires = [IS_STRONG(min=6, special=0.0, upper=0.0,number=0.0,lower=0.0),CRYPT()]
ouser.email.requires = [IS_EMAIL(error_message=userauth.messages.invalid_email),IS_NOT_IN_DB(db, ouser.email,error_message='E-mail address already in use')]
ouser.username.requires= [IS_NOT_EMPTY(error_message=userauth.messages.is_empty),IS_NOT_IN_DB(db, ouser.username,error_message='Username already taken')]
userauth.define_tables(username=True)
