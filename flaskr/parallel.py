import multiprocessing as mp
import time
from functools import partial

def random_square_fun(n, a, b):
    return n ** 2 + a[0] + b

if __name__ == "__main__":
    print(f"Number of cpu: {mp.cpu_count()}")

    t0 = time.time()
    n_cpu = mp.cpu_count()
    a_args = [1,2,3]

    pool = mp.Pool(processes=n_cpu)
    # results = [pool.map(random_square_fun, range(10000000))]
    results = [pool.map(partial(random_square_fun, a=a_args, b=a_args[2]), range(10000000))]
    t1 = time.time()
    print(f'Execution time {t1 - t0} seconds')
    print('First 10 results:', results[0][0:10])
