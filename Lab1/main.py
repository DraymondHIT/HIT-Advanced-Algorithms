from dataloader import DataLoader
from naive import Naive
import random
import time

n_samples = 200
c = 0.2

print('Data Loading:')
time_start = time.time()
corpus = DataLoader('./data/E1_AOL-out.txt').load()
time_end = time.time()
print('Data Loaded!')
print(f'Number of Set: {len(corpus.keys())}')
print(f'Time: {time_end-time_start}s')

print('Random Sampling:')
time_start = time.time()
samples = random.sample(corpus.items(), n_samples)
samples = {sample[0]: sample[1] for sample in samples}
time_end = time.time()
print(f'Number of Samples: {n_samples}')
print('Sampling Done!')

print('Naive Method Running:')
time_start = time.time()
naive = Naive()
result = naive.run(samples, c)
time_end = time.time()
print(f'Naive Method Result: {len(result)}')
print(f'Time: {time_end-time_start}s')
