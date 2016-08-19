# -*- coding: utf-8 -*-
if resauth.user:
    try :
        resauth.user.name
        session.flash='Please logout of \'Restaurant\' to continue'
        redirect(URL('restaurant','index'))
    except AttributeError:
        pass

if not session.gardenvars:
    session.gardenvars={}

try:
    type(userplate)
except NameError:
    userplate=Plate()
session.platecount=len(userplate.contents)

response.menu+=[['Homepage',False,URL('order','homepage')],['Help',False,None,[[['Item1'],False,None],['Item2',False,None]]]]

if userauth.user:
    response.menu=response.menu[:1]+[['My Previous Orders',False,None],['Account',False,None]]+response.menu[1:]

def index():
    redirect(URL('homepage'))

def homepage():
    response.title='Garden'
    response.subtitle='...'
    searchform=SQLFORM.factory(Field('name','reference city',requires=IS_IN_DB(db,db.city,label='%(name)s',error_message='Please select your city')),submit_button='Go!!!',labels=dict(name='Select your city'))
    if searchform.process().accepted:
        session.gardenvars['searchcity']=searchform.vars.name
        redirect(URL('searchfood'))
    elif searchform.errors:
        response.flash='Select your city'
    return dict(searchform=searchform)

def searchfood():
    if 'searchcity' not in session.gardenvars.keys():
        redirect(URL('homepage'))
    cityid=session.gardenvars['searchcity']
    #del session.gardenvars['searchcity']
    rows=db(db.resauth_user.id==cityid).select(db.resauth_user.ALL)
    return dict(rows=rows)

def user():
    form=userauth()
    return dict(form=form)

def seemenu():
    if not request.args:
        redirect(URL('searchfood'))
    resinfo=db(db.resauth_user.id==request.args(0)).select(db.resauth_user.ALL)
    if not len(resinfo)==1:
        session.flash='Error'
        redirect(URL('searchfood'))
    resinfo=resinfo.first()
    menuitems=db(db.dish.provider==request.args(0)).select(db.dish.ALL)
    return dict(resinfo=resinfo,menuitems=menuitems)

def seeitem():
    if not request.args:
        redirect(URL('order','searchfood'))
    iteminfo=db(db.dish.id==request.args(0)).select(db.dish.ALL)
    if not len(iteminfo)==1:
        session.flash='Error occoured'
        redirect(URL('order','searchfood'))
    iteminfo=iteminfo.first()
    return dict(iteminfo=iteminfo)

def see_plate():
    toret=[]
    for x in userplate.contents.keys():
        toret.append((db(db.dish.id==x).select(db.dish.ALL).first(),userplate.contents[x].item_count))
    return dict(totalcost=userplate.cost,itemlist=toret)

def storeplate():
    pf=pickleform(userplate)
    itemlist=[]
    for x in pf:
        itemlist.append((db(db.dish.id==x[0]).select(db.dish.ALL).first(),x[1]))
    form=FORM.confirm('Are you sure?',{'Back':URL('order','homepage')})
    if form.accepted:
        db.storedplate.insert(value=pickle.dumps(pf),type='saved')
        redirect(URL('order','homepage'))
    return dict(form=form,totalcost=userplate.cost,itemlist=itemlist)

def download_img():
    return response.download(request,db)
