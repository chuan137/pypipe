### PyPipe

Write lightweight coroutines in pipelines. (inspired by
[Ufo](https://github.com/ufo-kit/ufo-core) project.)

#### Features
  * decorators for feeder/workder/sinker
  * pipelines can be re-used


#### HowTo
Start using PyPipe in three simple steps:

First write a feeder/worker/sinker function, with corresponding factory decorator.

```python
@worker_fac
def mulitply(buf, factor):
    buf *= factor
    
@sinker_fac
def printer(buf):
    print buf
```

Then generate coroutines from above function factories and connect them into pipelines. **Note:** first arugument of worker/sinker are implicitly used in pipelines, ommit them in your code.

```python
w1 = multiply(2.0)
w2 = multiply(3.0)
prt = printer()

pipe = w1(w2(prt()))
```

Finally prepare a feeder, 

```python
@feeder_fac
def feed_ones(len):
    return np.ones(len)
    
fd = feed_ones([10,5,8])
```
and run the pipeline by attach them to it.
```python
fd(pipe())
```

#### ToDo
  * add pyopencl

#### Acknowledgement

<!--
*Ufo* is every reason that PyPipe exists. Ufo being simple and great, but ohnestly it is not quite light to use.  And the awful name, Hah! This is an effort to bring the essial part of Ufo to minimum python code. Kinergarden level. Yes, it is for **You**! 
-->

*Ufo* is every reason that PyPipe exists. Ufo being simple and great, but ohnestly it is not quite light to use. This is an effort to bring the essial part of Ufo to minimum python code.
