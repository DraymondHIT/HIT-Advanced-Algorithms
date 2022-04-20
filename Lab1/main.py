from dataloader import DataLoader
from naive import Naive
from minHash import MinHash
import random
import time
import numpy as np

n_samples = 500
b = 5
r = 4
# b_list = range(5, 35, 5)
# r_list = range(5, 10)
best = {"b": None, "r": None, "result": None, "value": 100000}
c = 0.5
FILE_PATH = './data/E1_kosarak_100k.txt'


def data(file_path):
    print('Data Loading...')
    time_start = time.time()
    corpus = DataLoader(file_path).load()
    time_end = time.time()
    print('Data Loaded!')
    print(f'Number of Set: {len(corpus.keys())}')
    print(f'Time: {time_end - time_start}s')
    return corpus


def sample(corpus, n_samples):
    print('Random Sampling...')
    time_start = time.time()
    samples = random.sample(corpus.items(), n_samples)
    samples = {sample[0]: sample[1] for sample in samples}
    time_end = time.time()
    print(f'Number of Samples: {n_samples}')
    print('Sampling Done!')
    print(f'Time: {time_end - time_start}s')
    return samples


def naiveMethod(samples, c):
    print('Naive Method Running...')
    time_start = time.time()
    naive = Naive()
    naive_result = naive.run(samples, c)
    time_end = time.time()
    print(f'Naive Method Result: {len(naive_result)}')
    print(f'Time: {time_end - time_start}s')
    return len(naive_result)


def preProcess(corpus):
    print('Preprocess...')
    time_start = time.time()
    keys = sorted(list(corpus.keys()))
    values = set()
    for value in corpus.values():
        values = values.union(value)
    values = sorted(list(values))
    value2index = dict()
    for i, element in enumerate(values):
        value2index[element] = i
    data = [[] for _ in range(len(keys))]
    for i in range(len(keys)):
        for element in corpus[keys[i]]:
            data[i].append(value2index[element])
    time_end = time.time()
    print('Done!')
    print(f'Time: {time_end - time_start}s')
    return data, len(values)


def minHashMethod(samples, n, b, r, naive_result):
    print('MinHash Method Running...')
    time_start = time.time()
    minHash = MinHash(b, r)
    minHash_result = minHash.run(samples, n)
    time_end = time.time()
    if abs(minHash_result - naive_result) < best["value"]:
        best["value"] = abs(minHash_result - naive_result)
        best["result"] = minHash_result
        best["b"] = b
        best["r"] = r
    print(f'b = {b} r = {r}')
    print(f'MinHash Method Result: {minHash_result}')
    print(f'Time: {time_end - time_start}s')


def main():
    corpus = data(FILE_PATH)
    samples = sample(corpus, n_samples)

    naive_result = naiveMethod(samples, c)
    # naive_result = []
    processed, n_elements = preProcess(samples)
    # for b in b_list:
    #     for r in r_list:
    #         minHashMethod(processed, n_elements, b, r, naive_result)

    minHashMethod(processed, n_elements, b, r, naive_result)
    # print(best)


if __name__ == '__main__':
    main()


