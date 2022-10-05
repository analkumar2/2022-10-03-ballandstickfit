import brute_curvefit as bcf
import numpy as np
import matplotlib.pyplot as plt

def funk(ttt=[1,2,3], x=1,y=1):
	return x+y

fitted, error = bcf.brute_scifit(
    funk,
    [1,2,3],
    10,
    restrict=[[0,0], [10,10]],
    ntol=1000,
    printerrors=True,
    parallel=True,
)

print(f'{fitted = }', f'{error}')