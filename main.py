import sqlite3
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
import re
import calendar

#needed: interface, table creation, table add row, table read row

#interface to add entry, add table, view in table, dump table, quit
def choosemode():
    val=raw_input('Create new tracker (C), Log(L), View(V), or Print(P)? Or quit(Q).')
    if len(val)>1:
        val=val[0]
    if val=='l' or val == 'L':
        return 'write'
    elif val=='v' or val == 'V':
        return 'query'
    elif val=='p' or val=='P':
        return 'dump'
    elif val=='c' or val=='C':
        return 'create'
    elif val=='q' or val=='Q':
        return 'quit'
    else:
        choosemode()

#reduce SQL injection vulnerability
def noninject(prompt):
    return ''.join(x for x in prompt if (x.isalnum or x==" " or x=='-' or x=="." or x==":") )

#CREATE: add a new table, checks for unique name. add the ability to exit
def addnewtable(c):
    tablename=noninject(raw_input("Please enter the name of the illness "))
    try:
        c.execute('CREATE TABLE {tn} (time text, duration text,rating real, other text)'.format(tn=tablename));
        print "Now tracking", tablename+"."
        return
    except sqlite3.OperationalError:
        print "That already exists. Use a different name."
        addnewtable(c)


def getdate():
    NOW=datetime.now()
    DATE_FORMAT="%a %b %d %Y at %H:%M"
    try:
        retval=parse(raw_input('date and time of illness? '), ignoretz=True, fuzzy=True, default=NOW)
    except ValueError:
        print "datefailed"
    try:
        print retval.strftime(DATE_FORMAT)
        return retval.strftime(DATE_FORMAT)
    except ValueError:
        print "Please clarify your input."
        getdate()

def getduration(e_date,inpstring):
    regexstring='(days)+|(day)+|(d)+|(hours)+|(hour)+|(hr)+|(hrs)+|(h)+|(minutes)+|(minute)+|(mins)+|(min)+|(m)+'
    durarr=filter(None,re.split(regexstring,inpstring,flags=re.IGNORECASE))
    length=len(durarr)
    e_date=datetime.strptime(e_date,"%a %b %d %Y at %H:%M")
    if length%2!=0 or length>6 or length==0: #strings that don't match won't work
        return ValueError 
    else:
        if length==6:
            return e_date+relativedelta(days=+int(durarr[0]),hours=+int(durarr[2]),minutes=+int(durarr[4]))
        elif length==4:
            if 'm' not in inpstring:
                return e_date+relativedelta(days=+int(durarr[0]),hours=+int(durarr[2]))
            if 'h' not in inpstring:
                return e_date+relativedelta(days=+int(durarr[0]),minutes=+int(durarr[2]))
            if 'd' not in inpstring:
                return e_date+relativedelta(hours=+int(durarr[0]),minutes=+int(durarr[2]))
        elif length==2:
            if 'd' in inpstring:
                return e_date+relativedelta(days=+int(durarr[0]))
            if 'h' in inpstring:
                return e_date+relativedelta(hours=+int(durarr[0]))
            if 'm' in inpstring:
                return e_date+relativedelta(minutes=+int(durarr[0]))

#WRITE: add a new entry to a given table.
def addentries(tablename,c):
    e_date=getdate()
    DATE_FORMAT="%a %b %d %Y at %H:%M"
    while True:
        try:
            e_duration_input=raw_input('duration of illness')
            e_duration=getduration(e_date,e_duration_input).strftime(DATE_FORMAT)
            break
        except ValueError:
            print "Please clarify your input in days, hours, and/or mintues"
    rating=int(raw_input('Rating of illness? 1-10 '))
    othernotes=noninject(raw_input('anything else to say? '))
    newentry=[e_date,e_duration,rating,othernotes]
    print "You were sick at", e_date, "until", e_duration, "with an intensity of", rating, ". Also,", othernotes+"."

    c.execute("INSERT INTO {tn} VALUES(?,?,?,?)".format(tn=tablename),newentry)




dbFilename='illnessdb.sqlite'

con= sqlite3.connect(dbFilename)
c=con.cursor()

c.execute("SELECT name from sqlite_master WHERE type='table'")
print "You are tracking these illnesses"
for x in c.fetchmany(100):
    print x[0]

mode='noidea'

while(mode!='quit'):
    mode=choosemode()
    if mode=='create':
        addnewtable(c)
    if mode=='query':
        pass
    if mode=='dump':
        pass
    if mode=='write':
        c.execute("SELECT name from sqlite_master WHERE type='table'")
        illnesses=[x[0] for x in c.fetchmany(100)]
        print "select an illness"
        for x in illnesses:
            print x
        tablename='totallyhealthymate'
        while tablename not in illnesses:
            tablename=raw_input("select a tracker ")
        addentries(tablename,c)



con.commit()
con.close()
