import time

def time_me(function):
    ''' a decorator that timing a function
    '''
    def wrap(*arg):
        start = time.time()
        r = function(*arg)
        end = time.time()
        print "%s (%0.3f ms)" % (function.func_name, (end-start)*1000)
        return r
    return wrap
