from set import MySet
from bloomFilter import BloomFilter
import math
from timeit import default_timer as timer

M = 100
N = 1000
K = int(math.log(2, math.e) * N / M)


def data():
    blacklist = set()
    for line in open('blacklist.txt'):
        blacklist.add(line.strip())
    return blacklist


def insertComparison(myset, bf):
    print('-------------------insert-------------------')
    names = {'James', 'Jack', 'Sue', 'Luis', 'Kevin', 'Charlotte', 'Leon', 'Neo', 'Destiny', 'Paul'}
    tic = timer()
    for name in names:
        myset.insert(name)
    toc = timer()
    print(f'Set Time: {(toc - tic)*1e6}us')
    tic = timer()
    for name in names:
        bf.insert(name)
    toc = timer()
    print(f'Bloom Filter Time: {(toc - tic)*1e6}us')


def findComparison(myset, bf):
    print('-------------------find-------------------')
    names = ['Nancy', 'Ella', 'Carl', 'Ben', 'Julia', 'Winston', 'Leo', 'Jessie', 'Destiny', 'Tommy']
    set_result = []
    bf_result = []
    tic = timer()
    for name in names:
        set_result.append(myset.find(name))
    toc = timer()
    print(f'Set Time: {(toc - tic)*1e6}us')
    tic = timer()
    for name in names:
        bf_result.append(bf.find(name))
    toc = timer()
    print(f'Bloom Filter Time: {(toc - tic)*1e6}us')
    print(set_result)
    print(bf_result)


def main():
    corpus = data()
    myset = MySet(corpus)
    bf = BloomFilter(corpus, K, N)
    insertComparison(myset, bf)
    findComparison(myset, bf)


if __name__ == "__main__":
    main()
