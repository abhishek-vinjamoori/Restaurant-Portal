# -*- coding: utf-8 -*-
from gluon.tools import Auth
import pickle
db=DAL('sqlite://storage.sqlite')
db.define_table('city',Field('name'),format='%(name)s')
db.define_table('category',Field('name',requires=IS_NOT_EMPTY(error_message='Please name the categry')),format='%(name)s')
