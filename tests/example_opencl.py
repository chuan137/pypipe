#!/usr/bin/env python
import numpy as np
import pyopencl as cl
from pypipe.decorator import feeder_fac, sinker_fac, worker_fac


def cl_contex(pid, did):
    platform = cl.get_platforms()[pid]    
    device = platform.get_devices()[did] 
    return cl.Context([device])

mf = cl.mem_flags

@worker_fac
def gpu_sum(buf, ctx, queue, prg):
    a_np, b_np = buf

    a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
    b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)
    res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
    prg.sum(queue, a_np.shape, None, a_g, b_g, res_g)
    res_np = np.empty_like(a_np)
    cl.enqueue_copy(queue, res_np, res_g)
    return res_np

@worker_fac
def cpu_sum(buf):
    a_np, b_np = buf
    return a_np + b_np


@feeder_fac
def feed_buffers(buf):
    return buf

@sinker_fac
def null_sinker(buf):
    #print buf
    pass
#------------------------------------------------------

def main():
    a_np = np.random.rand(500000).astype(np.float32)
    b_np = np.random.rand(500000).astype(np.float32)

    ctx = cl_contex(1,0)
    queue = cl.CommandQueue(ctx)
    prg = cl.Program(ctx, """
    __kernel void sum(__global const float *a_g, __global const float *b_g, __global float *res_g) {
      int gid = get_global_id(0);
      res_g[gid] = a_g[gid] + b_g[gid];
    }
    """).build()

    fd = feed_buffers([(a_np, b_np)])
    nul = null_sinker()
    gsum = gpu_sum(ctx, queue, prg)

    fd(gsum(nul()))

    fd2 = feed_buffers([(a_np, b_np)])
    csum = cpu_sum()

    fd2(csum(nul()))


#------------------------------------------------------
if __name__ == '__main__':
    main() 
