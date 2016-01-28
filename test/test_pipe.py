import numpy as np
import sys; sys.path.insert(0, '../')
from coroutines import *

def test_feeder():

    @feeder_fac
    def feed_ones(sz):
        return np.ones(sz)
    @sinker_fac
    def null_sinker(buf):
        pass

    buf_sizes = [ 10 ]

    fd = feed_ones(buf_sizes)
    nul = null_sinker()
    buf = fd(nul())

    assert (buf == np.ones(10)).all()


def test_address():
    '''Working buffer is passed between nodes by reference,
    therefore the address should be not altered'''
    class Msg(object):
        _addr1 = 1
        _addr2 = 2

    @feeder_fac
    def feed_ones(sz):
        buf = np.ones(sz)
        Msg._addr1 = buf.__array_interface__['data'][0]
        print 'Feeder:', Msg._addr1
        return buf

    @sinker_fac
    def null_sinker(buf):
        Msg._addr2 = buf.__array_interface__['data'][0]
        print 'Sinker:', Msg._addr2

    fd = feed_ones([ 10, 5 ])
    nul = null_sinker()
    buf = fd(nul())

    assert Msg._addr1 == Msg._addr2
