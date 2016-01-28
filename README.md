## PyPipe

Write lightweight coroutines in pipelines. (inspired by
[Ufo](https://github.com/ufo-kit/ufo-core) project.)

### Features
  * decorators for feeder/worker/sinker
  * pipelines can be re-used


### How To
Start using PyPipe in three simple steps:

* First write a feeder/worker/sinker function, with corresponding factory decorator.
```python
@worker_fac
def mulitply(buf, factor):
    buf *= factor
    
@sinker_fac
def printer(buf):
    print buf
```

* Then generate coroutines from above function factories and connect them into pipelines. *Note:* The first argument of worker/sinker factory are implicitly used in pipelines, omit them in your code.
```python
w1 = multiply(2.0)
w2 = multiply(3.0)
prt = printer()

pipe = w1(w2(prt()))
```

* Finally run the pipeline by attach them to a feeder. A feeder is created from a feeder factory, whose first argument must be a iterable. *Note:* Feeder is a function iterate over inputs, generate data and feed them into a pipeline. It is not a coroutine. Once it is consumed, it can not be used again. But the pipeline can be reused to consume another feeder.

```python
@feeder_fac
def feed_ones(len):
    return np.ones(len)
    
fd1 = feed_ones([10,5,8])
fd2 = feed_ones([100, 40])

fd1(pipe())
fd2(pipe())
```

For more details, please refer to tests/example.py in this git.

### ToDo
  * add pyopencl
  * add brancher maybe, but I think it is actually easier to handle branches in user space.

### Acknowledgement

<!--
*Ufo* is every reason that PyPipe exists. Ufo being simple and great, but it is not quite light to use.  And the awful name, Hah! This is an effort to bring the essential part of Ufo to minimum python code. Kinergarden level. Yes, it is for **You**! 
-->

**Ufo** is every reason that PyPipe exists. Ufo being simple and great, but it is not quite light to use. This is an effort to bring the essential part of Ufo to minimum python code.

For comprehension of the coroutine idea, I refer to David Beazley's [curious course](www.dabeaz.com/coroutines)
and original python enhancement proposal [PEP 342](https://www.python.org/dev/peps/pep-0342/).

