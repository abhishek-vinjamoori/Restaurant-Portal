# -*- coding: utf-8 -*-
if userauth.user:
    try :
        userauth.user.username
        session.flash='Please logout of \'User\' to continue'
        redirect(URL('order','homepage'))
    except AttributeError:
        pass

response.menu.append(['Homepage',False,URL('restaurant','index')])
if resauth.user:
    response.menu+=[['Manage Orders',False,URL('restaurant','manage_orders')],['Change Menu',False,URL('manage_menu')],['View Menu',False,URL('restaurant','view_menu')]]

def index():
    return dict(mesg=userauth.is_logged_in(),m2=resauth.user_id)

def user():
    return dict(form=resauth())

@resauth.requires_login()
def manage_menu():
    response.title='Manage your menu'
    addform=SQLFORM(db.dish)
    if addform.process().accepted:
        response.flash='%s has been added to the menu' %(addform.vars.name)
    elif addform.errors:
        response.flash='Please correct the errors and try again'
    modifyform=SQLFORM.factory(Field('name','reference\
                               dish',requires=IS_IN_DB(db(db.dish.provider==resauth.user_id),db.dish,label='%(name)s',error_message='Select an item to modify')),
                               Field('price',requires=IS_EMPTY_OR(IS_INT_IN_RANGE(17,None))),
                               Field('description',length=1024),
                               Field('image','upload',requires=IS_EMPTY_OR(IS_IMAGE(error_message='Uploaded file must be\
                               an image'))),
                               table_name='modifyform_dummy_table')
    if modifyform.process().accepted:
     #   try:
        dicty={}
        if modifyform.vars.price:
            dicty['price']=modifyform.vars.price
        if modifyform.vars.description:
            dicty['description']=modifyform.vars.description
        if modifyform.vars.image:
            dicty['image']=modifyform.vars.image
        db(db.dish.id==modifyform.vars.name).update(**dicty)
        response.flash='Sucessfully updated'
       #except:
       #response.flash='Unexpected error occoured'
    elif modifyform.errors:
        response.flash='Please correct the errors'
    delform=SQLFORM.factory(Field('name','reference dish',requires=IS_IN_DB(db(db.dish.provider==resauth.user_id),db.dish,label='%(name)s',error_message='Please select an item to delete')),
                            table_name='delform_dummy_table')
    if delform.process().accepted:
        dishname=db.dish[delform.vars.name].name
        del db.dish[delform.vars.name]
        response.flash='%s deleted from the menu' %(dishname)
    elif delform.errors:
        response.flash='Did not delete item due to errors'
    return dict(addform=addform,modifyform=modifyform,delform=delform)

@resauth.requires_login()
def manage_orders():
    q=db.dish.provider==resauth.user_id
    q&=db.dish.id==db.orders.item_id
    rows=db(q).select(db.orders.ALL,db.dish.ALL)
    return dict(rows=rows)

@resauth.requires_login()
def view_menu():
    response.title='Your Menu'
    response.subtitle='tasty...'
    rows=db(db.dish.provider==resauth.user_id).select(db.dish.ALL)
    return dict(rows=rows)
def download_img():
    return response.download(request,db)
