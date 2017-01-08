from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *


def noninject(prompt):
    return ''.join(x for x in prompt if (x.isalnum or x==" " or x=='-' or x=="." or x==":") )

def getdate(promptstring):
    NOW=datetime.now()
    DATE_FORMAT="%Y-%m-%d %H:%M:%S"#"%a %b %d %Y at %H:%M"
    try:
        retval=parse(noninject(raw_input(promptstring+ ' ')), ignoretz=True, fuzzy=True, default=NOW)
    except ValueError:
        print "datefailed"
    try:
        #print retval.strftime(DATE_FORMAT)
        return retval.strftime(DATE_FORMAT)
    except ValueError:
        print "Please clarify your input."
        getdate(promptstring)
