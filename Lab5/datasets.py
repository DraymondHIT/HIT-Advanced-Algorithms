import os
import pickle5 as pickle
from urllib.request import urlretrieve


def download(src, dst):
    if not os.path.exists(dst):
        # TODO: should be atomic
        print('downloading %s -> %s...' % (src, dst))
        urlretrieve(src, dst)


def get_dataset_fn(dataset):
    if not os.path.exists('data'):
        os.mkdir('data')
    return os.path.join('data', '%s.pickle' % dataset)


def get_dataset(which):
    fn = get_dataset_fn(which)
    if not os.path.exists(fn):
        url = 'http://itu.dk/people/maau/fairnn/datasets/%s.pickle' % which
        download(url, fn)
    with open(fn, 'rb') as f:
        data, queries, ground_truth, attrs = pickle.load(f)
    return data, queries, ground_truth, attrs
