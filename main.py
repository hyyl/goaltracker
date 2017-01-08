import sqlite3
from createentry import addentries, noninject
from querytable import dumptable

#needed: interface, table creation, table add row, table read row

#interface to add entry, add table, view in table, dump table, quit
def chooseinitmode():
    val=raw_input('Create new tracker (C) or select an already existing tracker(S)? Or quit(Q).')
    if len(val)>1:
        val=val[0]
    if val=='s' or val == 'S':
        return 'select'
    elif val=='c' or val=='C':
        return 'create'
    elif val=='q' or val=='Q':
        return 'quit'
    else:
        chooseinitmode()

def choosetablemode():
    val=raw_input('Log(L), view some values(V), or dump all values(P)? Or quit(Q).')
    if len(val)>1:
        val=val[0]
    if val=='l' or val == 'L':
        return 'write'
    elif val=='v' or val == 'V':
        return 'query'
    elif val=='p' or val=='P':
        return 'dump'
    elif val=='q' or val=='Q':
        return 'quit'
    else:
        choosetablemode()


#CREATE: add a new table, checks for unique name. add the ability to exit
def addnewtable(c):
    tablename=noninject(raw_input("Please enter the name of the illness "))
    try:
        c.execute('CREATE TABLE {tn} (time TIMESTAMP, duration TIMESTAMP,rating INTEGER, other TEXT)'.format(tn=tablename));
        print "Now tracking", tablename+"."
        return
    except sqlite3.OperationalError:
        print "That already exists. Use a different name."
        addnewtable(c)


def selecttable(c):
    c.execute("SELECT name from sqlite_master WHERE type='table'")
    illnesses=[x[0] for x in c.fetchall()]
    if len(illnesses)==0:
        return None
    print "select an illness"
    for x in illnesses:
        print x
    tablename='totallyhealthymate'
    while tablename not in illnesses:
        tablename=raw_input("select a tracker ")
    return tablename


dbFilename='illnessdb.sqlite'

conn= sqlite3.connect(dbFilename,detect_types=sqlite3.PARSE_DECLTYPES)
c=conn.cursor()

c.execute("SELECT name from sqlite_master WHERE type='table'")
print "You are tracking these illnesses"
for x in c.fetchmany(100):
    print x[0]

mode='noidea'
tablemode='noidea'

while(mode!='quit'):
    mode=chooseinitmode()
    if mode=='create':
        addnewtable(c)
    if mode=='select':
        tablename=selecttable(c)
        if tablename!=None:
            while (tablemode!='quit'):
                tablemode=choosetablemode()
                if tablemode=='query':
                    pass
                if tablemode=='dump':
                    dumptable(tablename,conn)
                if tablemode=='write':
                    addentries(tablename,c)



conn.commit()
conn.close()
