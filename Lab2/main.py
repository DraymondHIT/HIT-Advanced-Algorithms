from data import DataGenerator
from naive import Naive
from linear import Linear
import time

N_SAMPLES = 10000
K = 5000


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
    print('Naive Method Running...')
    time_start = time.time()
    naive = Naive(corpus, k)
    result = naive.run(["uniform", "normal", "zipf"])
    time_end = time.time()
    print('===========Naive Method Result===========')
    printDict(result)
    print(f'Time: {time_end - time_start}s')


def linearMethod(corpus, k):
    print('Linear Method Running...')
    time_start = time.time()
    linear = Linear(corpus, k)
    result = linear.run(["uniform", "normal", "zipf"])
    time_end = time.time()
    print('===========Linear Method Result===========')
    printDict(result)
    print(f'Time: {time_end - time_start}s')


def main():
    corpus = data(N_SAMPLES)
    naiveMethod(corpus, K)
    linearMethod(corpus, K)


if __name__ == "__main__":
    main()
