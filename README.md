## PyPipe

Write lightweight pipeline with coroutines. (inspired by
[Ufo](https://github.com/ufo-kit/ufo-core) project.)

### Features
  * Easy to use, decorators for feeder/worker/sinker
  * compatible with pyopencl, pycuda

### How To
Use PyPipe in three simple steps:

* First step. Write worker/sinker/feeder functions with corresponding factory
  decorator.  

```python
@worker_fac
def mulitply(buf, factor):
    buf *= factor
    
@sinker_fac
def printer(buf):
    print buf

@feeder_fac
def feed_ones(len):
    return np.ones(len)
```

* Then generate coroutines from above function factories and connect them into
  pipelines. 

```python
w1 = multiply(2.0)
w2 = multiply(3.0)
prt = printer()

pipe = w1(w2(prt()))
```

> *Note:* The first argument of worker/sinker factory are implicitly used by
> decorator functions. Omit them when generating.

* Finally run the pipeline by attach them to a feeder. Feeder iterates over
  inputs, generate data and feed them into a pipeline. Feeder is not
a coroutine, and it does not yield control to other routines. Once it is
consumed by a pipeline, the function is executed and returns. By contrast, the
pipeline processes data and yield its control. A Piepleine can consume many
feeders as long as it is not stopped manually. 

```python
fd1 = feed_ones([10,5,8])
fd2 = feed_ones([100, 40])

fd1(pipe())
fd2(pipe())
```

>  *Note*: the first argument of a feeder factory is transformed to a iterable
>  by the seeder decorator.

More details can be found in tests/example.py.

### ToDo
  * add brancher
  * multiple processes (how)
  * stop pipeline (?) 

### Acknowledgement

<!--
*Ufo* is every reason that PyPipe exists. Ufo being simple and great, but it is not quite light to use.  And the awful name, Hah! This is an effort to bring the essential part of Ufo to minimum python code. Kinergarden level. Yes, it is for **You**! 
-->

<!--
**Ufo** is every reason that PyPipe exists. Ufo being simple and great, but it is not quite light to use. This is an effort to bring the essential part of Ufo to minimum python code.
-->

For comprehension of the coroutine idea, I have refered to David Beazley's [curious course](www.dabeaz.com/coroutines)
and original python enhancement proposal [PEP 342](https://www.python.org/dev/peps/pep-0342/).

