from data import DataGenerator
from naive import Naive
from linear import Linear
from lazySelect import LazySelect
import numpy as np
import time

N_SAMPLES = 1000
K = 500


def printDict(dic):
    for key in dic.keys():
        print(f"{key}: {dic[key]}")


def data(n_samples):
    print('Data Loading...')
    time_start = time.time()
    corpus = DataGenerator(n_samples).load()
    time_end = time.time()
    print('Data Loaded!')
    print(f'Number of Samples: {len(corpus)}')
    print(f'Time: {time_end - time_start}s')
    return corpus


def naiveMethod(corpus, k):
    time_start = time.time()
    naive = Naive(corpus, k)
    result = naive.run(["uniform", "normal", "zipf"])
    time_end = time.time()
    print('===========Naive Method Result===========')
    printDict(result)
    print(f'Time: {time_end - time_start}s')
    return result, time_end - time_start


def linearMethod(corpus, k):
    time_start = time.time()
    linear = Linear(corpus, k)
    result = linear.run(["uniform", "normal", "zipf"])
    time_end = time.time()
    print('===========Linear Method Result===========')
    printDict(result)
    print(f'Time: {time_end - time_start}s')
    return time_end - time_start


def lazyMethod(corpus, k):
    time_start = time.time()
    lazy = LazySelect(corpus, k)
    result = lazy.run(["uniform", "normal", "zipf"])
    time_end = time.time()
    print('===========Lazy Method Result===========')
    printDict(result)
    print(f'Time: {time_end - time_start}s')
    return result, time_end - time_start


def main():
    corpus = data(N_SAMPLES)
    naiveTime = []
    linearTime = []
    lazyTime = []
    error = 0
    for _ in range(10):
        print(f'=============Epoch {_+1}=============')
        correct, time = naiveMethod(corpus, K)
        naiveTime.append(time)
        linearTime.append(linearMethod(corpus, K))
        result, time = lazyMethod(corpus, K)
        lazyTime.append(time)
        error += int(correct["uniform"] != result["uniform"]) \
                 + int(correct["normal"] != result["normal"]) \
                 + int(correct["zipf"] != result["zipf"])
    print('=============Conclusion=============')
    print(f"Naive: {np.mean(naiveTime)}")
    print(f"Linear: {np.mean(linearTime)}")
    print(f"Lazy: {np.mean(lazyTime)}")
    print(f"Accuracy: {1. - error/30.}")


if __name__ == "__main__":
    main()
