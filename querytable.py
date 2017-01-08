import sqlite3
from datetime import *
from dateutil.relativedelta import *
from dateutil.parser import *
from getdate import *

def calcdurhr(begin,end):
    #print begin, end
    #begin=datetime.strptime(begin,"%Y-%m-%d %H:%M:%S")
    #end=datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
    t=relativedelta(end,begin)
    return t.days*24+t.hours+t.minutes/60.0


#all = all
def dumptable(tablename,conn,mode):
    conn.row_factory=sqlite3.Row
    r=conn.cursor()
    if mode=='all':
        r.execute('select * from {tn} ORDER BY time ASC, duration ASC'.format(tn=tablename))
    if mode=='range':
        beginrange=getdate("Beginning of range")
        endrange=getdate("end of range")
        r.execute('select * from {tn} WHERE time BETWEEN ? AND ? ORDER BY time ASC, duration ASC'.format(tn=tablename),(beginrange,endrange,))
    entries=r.fetchall()
    avgdurhr=0
    count=0
    if mode=='all':
        print "    Complete Log for", tablename
    if mode=='range':
        print "    Log for", tablename, "between", beginrange, endrange
    print "|  start time                | elapsed (hr) |rating"
    #      |  Thu Dec 29 2016 at 21:37  |        0.05  |  10
    for e in entries:
        elapsed=calcdurhr(e['time'],e['duration'])
        lenstr=9-len(str(elapsed))
        print "| ", datetime.strftime(e['time'],"%a %b %d %Y at %H:%M"), " | ", " "*lenstr, "%0s" %elapsed, " | ", e['rating']
        avgdurhr+=elapsed
        count+=1
    if count !=0:
        print "average hours were " + str(avgdurhr/count)
