def count():
    message="THe number of visitors for this page are:\n"
    if not session.counter:
        session.counter=1
    else:
        session.counter+=1
    var=session.counter
    return locals()

def page_one():
    return dict(mess="First page is being displayed.\n")
def page_two():
    return dict(mess="Second page is being displayed\n")
def page_three():
    return dict(mess="Third page is being displayed\n")
