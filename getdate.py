from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *



def getdate(promptstring):
    NOW=datetime.now()
    DATE_FORMAT="%Y-%m-%d %H:%M:%S"#"%a %b %d %Y at %H:%M"
    try:
        retval=parse(raw_input(promptstring+ ' '), ignoretz=True, fuzzy=True, default=NOW)
    except ValueError:
        print "datefailed"
    try:
        #print retval.strftime(DATE_FORMAT)
        return retval.strftime(DATE_FORMAT)
    except ValueError:
        print "Please clarify your input."
        getdate(promptstring)
