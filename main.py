import sqlite3
from createentry import addentries
from querytable import dumptable, noninject


#interface to add entry, add table, view in table, dump table, quit
def chooseinitmode():
    val=raw_input('Create new tracker (C), delete a tracker (D) or select an already existing tracker(S)? Or quit(Q).')
    if len(val)>1:
        val=val[0]
    if val=='s' or val == 'S':
        return 'select'
    elif val=='c' or val=='C':
        return 'create'
    elif val=='d' or val=='D':
        return 'delete'
    elif val=='q' or val=='Q':
        return 'quit'
    else:
        chooseinitmode()

def choosetablemode():
    val=raw_input('Log(L), view entries within a date range(D), view the most recent entries(X) or dump all values(P)? Or quit(Q).')
    if len(val)>1:
        val=val[0]
    if val=='l' or val == 'L':
        return 'write'
    elif val=='d' or val == 'D':
        return 'datequery'
    elif val=='x' or val == 'X':
        return 'xquery'
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
                if tablemode=='datequery':
                    dumptable(tablename,conn,'daterange')
                if tablemode=='xquery':
                    dumptable(tablename,conn,'norange')
                if tablemode=='dump':
                    dumptable(tablename,conn,'all')
                if tablemode=='write':
                    addentries(tablename,c)
                conn.commit() #commit in case of run errors
        print "no tables currently exist"
    if mode=='delete':
        tablename=selecttable(c)
        if tablename!=None:
            val=raw_input('Would you like to delete table:'+tablename+'? (Y) to confirm.')
            if len(val)>1:
                val=val[0]
            if val=='y' or val == 'Y':
                c.execute('DROP TABLE {tn}'.format(tn=tablename))
        print "no tables currently exist"



conn.commit()
conn.close()
