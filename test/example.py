import numpy as np
from time_me import time_me
import sys; sys.path.insert(0, '../')
from coroutines import *

# a factory generate a filter of some type: feeder, worker or sinker
#
# when defining a worker_/sinker_fac, the first arg must be reference to the
# working  buffer. when using, the first argument (working buffer) is
# concealed, similarly to  a class function concealing the `self` argument.
#
# A feeder should iterate over a iterable, which is the first argument in
# calling. When defining, the first argument should be of type of the
# content of the iterable.
# A feeder returns the working buffer in the final (processed) state.

# worker and sinker factory:
# 1. first argument is proceesing buffer, used implicitly in calling
# 2. second arguments and on are used in generating a worker/sinker
@worker_fac
def multiply(buf, factor=1.0):
    buf *= factor

@sinker_fac
def printer(buf):
    print "Printer:", buf

@sinker_fac
def null_sinker(buf):
    pass

@feeder_fac
def feed_ones(sz):
    return np.ones(sz)

def main():
    rep_num = 1
    sizes = [ 10 ]

    # generate coroutines from the coroutine factories
    # 1. workers w1(*), w2(*) ... and sinkers pnt(), nul() returns a generator
    # 2. first argument (working buffer) is concealed
    # 3. worker connect to next node via its argument, which is a generator
    # 4. sinker does not have a next node
    w1 = multiply(2)
    w2 = multiply(3)
    w3 = multiply(-1)
    prt = printer()
    nul = null_sinker()

    # feeders iterate over a iterable, and feed the pipeline
    # 1. feeder returns the working buffer in the final state
    # 2. like worker, feeder connects to next node via its argument
    # 3. feeder can't be re-uesed, they are done once the iterations done
    feeders = [feed_ones(sizes) for i in range(rep_num)]

    # first generate coroutines from coroutine factories
    # pipeline can be re-use with different feeder
    p = w1(w2(w3(prt())))

    @time_me
    def _run():
        for fd in feeders:
            buf = fd(p)
            print buf

    _run()


if __name__ == '__main__':
    main()
