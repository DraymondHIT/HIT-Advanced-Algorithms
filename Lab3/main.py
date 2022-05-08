from set import MySet
from bloomFilter import BloomFilter
import math
import random
import string
from timeit import default_timer as timer

epsilon = 1e-2
M = 29717
N = int(- M * math.log(epsilon) / math.log(2) / math.log(2))
K = int(math.log(2, math.e) * N / M)


def data():
    blacklist = set()
    for line in open('blacklist.txt'):
        blacklist.add(line.strip())
    return blacklist


def test_generator(data):
    test = random.sample(data, 500)
    for _ in range(500):
        len = random.randint(3, 10)
        random_str = ''.join(random.choice(string.ascii_letters) for _ in range(len))
        test.append(random_str)
    return test


def insertComparison(myset, bf):
    print('-------------------insert-------------------')
    names = {'james', 'jack', 'sue', 'luis', 'kevin', 'charlotte', 'leon', 'neo', 'destiny', 'paul'}
    tic = timer()
    for name in names:
        myset.insert(name)
    toc = timer()
    print(f'Set Time: {(toc - tic)*1e6/len(names)}us')
    tic = timer()
    for name in names:
        bf.insert(name)
    toc = timer()
    print(f'Bloom Filter Time: {(toc - tic)*1e6/len(names)}us')


def findComparison(names, myset, bf):
    print('-------------------find-------------------')
    set_result = []
    bf_result = []
    tic = timer()
    for name in names:
        set_result.append(myset.find(name))
    toc = timer()
    print(f'Set Time: {(toc - tic)*1e6/len(names)}us')
    tic = timer()
    for name in names:
        bf_result.append(bf.find(name))
    toc = timer()
    print(f'Bloom Filter Time: {(toc - tic)*1e6/len(names)}us')
    count = 0
    for i in range(len(set_result)):
        if set_result[i] == bf_result[i]:
            count += 1
    print(f'Accuracy: {float(count)/len(set_result)}')


def main():
    corpus = data()
    myset = MySet(corpus)
    bf = BloomFilter(corpus, K, N)
    insertComparison(myset, bf)
    test = test_generator(corpus)
    findComparison(test, myset, bf)


if __name__ == "__main__":
    main()
