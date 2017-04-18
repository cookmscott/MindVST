from hyperopt import fmin, tpe, hp

space=hp.uniform('x', -10, 10)

def print_func(x):
    print x
    return x ** 2

best = fmin(print_func,
    space=hp.quniform('x', 0, 1, 0.01),
    algo=tpe.suggest,
    max_evals=100)
print best