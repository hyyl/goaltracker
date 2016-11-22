import sqlite3

def yesorno():
    val=raw_input()
    val=val[0]
    if val=='y' or val=='Y':
        return 1
    elif val=='n' or val=='N':
        return 0
    else:
        return -1

def noninject(prompt):
    return ''.join(x for x in prompt if (x.isalnum or x==" " or x=='-' or x=="." or x==":") )

def addnew(c):
    tablename=noninject(raw_input("Please enter the name of the illness "))
    try:
        c.execute('CREATE TABLE {tn} (date text,time text, rating real, other text)'.format(tn=tablename));
        print "Now tracking", tablename+"."
        return
    except sqlite3.OperationalError:
        print "That already exists. Use a different name."
        addnew(c)
    
def addentries(tablename,c):
    e_date=raw_input('date of illness? ')
    e_time=raw_input('time of illness? ')
    rating=int(raw_input('Rating of illness? 1-10 '))
    othernotes=noninject(raw_input('anything else to say? '))
    newentry=[tablename,e_date,e_time,rating,othernotes]
    print "You were sick at", e_date, e_time, "with an intensity of", rating, ". Also,", othernotes+"."
    c.execute("INSERT INTO ? VALUES(?,?,?,?)",newentry)


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
        addnew(c)
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



conn.commit()
conn.close()
PROMPT_INVALID=True
mode=''

while(PROMPT_INVALID):
    PROMPT_INVALID=False
    val=raw_input('Log(L), View(V), or Print(P)?')
    if val=='l' or val == 'L':
        mode='write'
    elif val=='v' or val == 'V':
        mode='query'
    elif val=='p' or val=='P':
        mode='dump'
    else:
        PROMPT_INVALID=true;


conn= sqlite3.connect(dbFilename)
c=conn.cursor()

if mode=='write':
    date=raw_input('date of illness? ')
    time=raw_input('time of illness? ')
    rating=input('Rating of illness? 1-10 ')
    othernotes=raw_input('anything else to say? ')
    print "You were sick at", date, time, "with an intensity of", rating, ". Also,", othernotes, "."
    
'''
