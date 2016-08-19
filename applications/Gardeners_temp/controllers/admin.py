# -*- coding: utf-8 -*-
import socket
import gluon.fileutils
http_host=request.env.http_host.split(':')[0]
remote_addr=request.env.remote_addr
try:
    hosts=(http_host, socket.gethostname(),socket.gethostbyname(http_host),'::1', '127.0.0.1', '::ffff:127.0.0.1')
except:
    hosts=(http_host,)

if request.is_https:
    session.secure()
elif (remote_addr not in hosts) and (remote_addr != "127.0.0.1"):
    raise HTTP(200, T('admin is disabled because channel is insecure'))

if (request.application == 'admin' and not session.authorized) or (request.application != 'admin' and not gluon.fileutils.check_credentials(request)):
    redirect(URL('admin', 'default', 'index',
                 vars=dict(send=URL(args=request.args, vars=request.vars))))

response.view='admin.html'
menu=True
if menu:
    response.menu=[[B('Homepage'),False,URL('order','homepage')],['Manage Users',True,URL('muser')],['Manage Restaurants',False,URL('mres')],['Service Management',False,URL('moth')]]
def index():
    return dict()
def mres():
    button=0
    form=None
    #awer
    def changebutton(new_value):
        global button
        button=new_value
        if button==1:
            form='a'
        elif button==2:
            form=231
        elif button==3:
            form=23
        else:
            form=None
        return dict(button=button)
    return dict(changebutton=changebutton,button=button,form=form)
def muser():
    return dict()
def moth():
    addform=SQLFORM.factory(Field('city_name',
                                  requires=[IS_NOT_EMPTY(error_message='Please enter a city\
                                  name'),IS_MATCH('^[A-Z][a-z]*$',error_message='Make sure that the name start in capital\
                                  and contains only\
                                  alphabets'),IS_NOT_IN_DB(db,db.city.name,error_message='City already included')]),
                            table_name='addform_dummy_table')
    if addform.process().accepted:
        try:
            db.city.insert(name=addform.vars.city_name)
        except:
            response.flash='Unexpected error occoured'
        else:
            response.flash='City name %s added to city list' %(addform.vars.city_name)
    elif addform.errors:
        response.flash='Please try again'
    delform=SQLFORM.factory(Field('city','reference city',requires=IS_IN_DB(db,db.city,label='%(name)s',error_message='Select a city to delete')),
                            table_name='delform_dummy_table')
    if delform.process().accepted:
            cityname=db.city[delform.vars.city].name
            del db.city[delform.vars.city]
            response.flash='Successfull deleted %s from list of cities' %(cityname)
    elif delform.errors:
            response.flash='Correct the errors and try to delete again'
    return dict(addform=addform,delform=delform)
