from dataloader import DataLoader
from naive import Naive
from minHash import MinHash
import random
import time

n_samples = 500
b = 5
r = 4
# b_list = range(5, 35, 5)
# r_list = range(5, 10)
best = {"b": None, "r": None, "result": None, "value": 100000}
c = 0.8
FILE_PATH = './data/E1_AOL-out.txt'


def data(file_path):
    print('Data Loading...')
    time_start = time.time()
    corpus = DataLoader(file_path).load()
    time_end = time.time()
    print('Data Loaded!')
    print(f'Number of Set: {len(corpus)}')
    print(f'Time: {time_end - time_start}s')
    return corpus


def sample(corpus, n_samples):
    print('Random Sampling...')
    time_start = time.time()
    samples = random.sample(corpus, n_samples)
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

    data1 = []
    data2 = []
    flag = 0
    for i in range(0, len(corpus) - 1, 2):
        data1.append(list(set(corpus[i]).union(set(corpus[i + 1]))))
    if len(corpus) % 2 != 0:
        data1.append(list(set(corpus[-1])))
    while True:
        if flag == 0:
            for j in range(0, len(data1) - 1, 2):
                data2.append(list(set(data1[j]).union(set(data1[j + 1]))))
            if len(data1) % 2 != 0:
                data2.append(list(set(data1[-1])))
            if len(data2) == 1:
                random.shuffle(data2[0])
                values = data2[0]
                break
            data1 = []
            flag = 1
        if flag == 1:
            for j in range(0, len(data2) - 1, 2):
                data1.append(list(set(data2[j]).union(set(data2[j + 1]))))
            if len(data2) % 2 != 0:
                data1.append(list(set(data2[-1])))
            if len(data1) == 1:
                random.shuffle(data1[0])
                values = data1[0]
                break
            data2 = []
            flag = 0

    values = sorted(list(values))
    value2index = dict()
    for i, element in enumerate(values):
        value2index[element] = i
    data = [[] for _ in range(len(corpus))]
    for i in range(len(corpus)):
        for element in corpus[i]:
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
    # if abs(minHash_result - naive_result) < best["value"]:
    #     best["value"] = abs(minHash_result - naive_result)
    #     best["result"] = minHash_result
    #     best["b"] = b
    #     best["r"] = r
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


