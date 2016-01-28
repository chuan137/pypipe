import traceback as tb
import numpy as np
import time

def feeder_fac(func):
    def wrapper(iterable):
        iterable = iter(iterable)
        def feeder(target):
            target.send(None)
            try:
                start = time.time()
                while 1:
                    n = iterable.next()
                    _buffer = func(n)
                    target.send(_buffer)
            except StopIteration:
                runtime = time.time() - start
                print 'Feeder: done (%0.3f ms)' % (1000 *(runtime))
            return _buffer
        return feeder
    return wrapper

def worker_fac(func):
    def wrapper(*args, **kwargs):
        def worker(target):
            target.send(None)
            while 1:
                try:
                    _buffer = (yield)
                    func(_buffer, *args, **kwargs)
                    target.send(_buffer)
                except StopIteration as e:
                    print 'iteration stopped'
                    raise e
                except TypeError:
                    pass
        return worker
    return wrapper

def sinker_fac(func):
    def wrapper(*args, **kwargs):
        def sinker():
            while 1:
                try:
                    _buffer = (yield)
                    func(_buffer, *args, **kwargs)
                except StopIteration as e:
                    print 'iteration stopped'
                    raise e
                except TypeError:
                    pass
        return sinker
    return wrapper
