import sys, logging


class LogPrinter:
    '''LogPrinter class which serves to emulates a file object and logs
       whatever it gets sent to a Logger object at the INFO level.'''
    def __init__(self):
        '''Grabs the specific logger to use for logprinting.'''
        self.ilogger = logging.getLogger('logprinter')
        il = self.ilogger
        logging.basicConfig()
        il.setLevel(logging.INFO)

    def write(self, text):
        '''Logs written output to a specific logger'''
        self.ilogger.info(text)

def logprintinfo(func):
    '''Wraps a method so that any calls made to print get logged instead'''
    def pwrapper(*arg, **kwargs):
        stdobak = sys.stdout
        lpinstance = LogPrinter()
        sys.stdout = lpinstance
        try:
            return func(*arg, **kwargs)
        finally:
            sys.stdout = stdobak
    return pwrapper
