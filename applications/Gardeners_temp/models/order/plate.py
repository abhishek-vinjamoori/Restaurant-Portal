# -*- coding: utf-8 -*-
class Item:
    def __init__(this,item_id,quantity=1):
        this.item_id=item_id
        this.item_row=db.dish[this.item_id]
        this.item_name=this_query.name
        this.item_count=quantity
        this.item_sprice=int(this.item_row.price)
        this.item_tprice=this.item_sprice*this.item_count

class Plate:
    def __init__(this):
        this.contents={}
        this.cost=0
    def remove(this,tosub):
        this.cost-=this.contents[tosub].item_tprice
        del this.contents[tosub]
    def __add__(this,toadd):
        if type(toadd)==tuple:
            if toadd[0] in this.contents.keys():
                this.remove(toadd[0])
                this+=toadd
            else:
                this.contents[toadd[0]]=Item(toadd[0],toadd[1])
                this.cost+=this.contents[toadd[0]].item_tprice
        elif type(toadd)==type(this):
            for x in toadd.contents.keys():
                    this+=(x,toadd.contents[x].item_count)
        else:
            raise TypeError('Cannot add %(type(toadd))s to %(type(this))s')

def pickleform(value):
    toret=[]
    dict=value.contents
    for x in dict.keys():
        toret.append((x,dict[x].item_count))
    return toret

def gardenform(value):
    toret=Plate()
    for x in value:
        toret.contents[x[0]]=Item(x[0],x[1])
        toret.cost+=toret.contents[x[0]].item_tprice
    return toret

def addtoplate(item_id,item_count=1,mode='normal'):
    if mode=='normal':
        userplate+=(item_id,item_count)
    else:
        userplate+=item_id

db.define_table('storedplate',
                 Field('time','datetime',writable=False,default=request.now),
                 Field('owner','reference auth_user',writable=False,default=userauth.user_id),
                 Field('type',requires=IS_IN_SET(('saved','bought'),error_message='Error.Type not defined'),default='bought'),
                 Field('value','text'))
