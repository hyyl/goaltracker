import sqlite3

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
        c.execute('CREATE TABLE {tn} (date text,time text, rating real, other text)'.format(tn=tablename));
        print "Now tracking", tablename+"."
        return
    except sqlite3.OperationalError:
        print "That already exists. Use a different name."
        addnewtable(c)

#WRITE: add a new entry to a given table.
def addentries(tablename,c):
    e_date=raw_input('date of illness? ')
    e_time=raw_input('time of illness? ')
    rating=int(raw_input('Rating of illness? 1-10 '))
    othernotes=noninject(raw_input('anything else to say? '))
    newentry=[e_date,e_time,rating,othernotes]
    print "You were sick at", e_date, e_time, "with an intensity of", rating, ". Also,", othernotes+"."
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
