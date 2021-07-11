import numpy as np
a = np.arange(10)
print(a)
b = sum(a)
%timeit sum(a)
%timeit np.sum(a)
print(b)
