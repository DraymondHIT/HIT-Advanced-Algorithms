import os
import pickle
import time
import numpy as np
from lsh import LSHBuilder
import matplotlib.pyplot as plt


def result_prob(results):
    probs = {}
    for q, res in results.items():
        probs[q] = []
        cnts = {}
        for r in res:
            if r != -1:
                cnts.setdefault(r, 0)
                cnts[r] += 1
        n = sum(cnts.values())
        p = [[r, cnts[r]/n] for r in cnts]
        probs[q] = p
    return probs


def total_variation_dist(g, res):
    all = np.zeros(len(g))
    for i in range(len(g)):
        n = int(1/g[i])
        r = np.array([p for _, p in res[i]] + [0] * (n - len(res[i])))
        all[i] = 0.5 * np.sum(np.abs(r - g[i]))
    return np.mean(all)


def get_result_fn(dataset, query_type, rep):
    if not os.path.exists(os.path.join("results", dataset, query_type)):
        os.makedirs(os.path.join("results", dataset, query_type))
    return os.path.join(os.path.join("results", dataset, query_type, rep + ".pickle"))


def get_variation_dist(data, path):
    tvd_result = []
    for method in LSHBuilder.methods:
        if os.path.exists(os.path.join("results", data, method, path + ".pickle")):
            with open(os.path.join("results", data, method, path + ".pickle"), 'rb') as f:
                res_dict = pickle.load(f)
                prob = result_prob(res_dict["res"])
                groundtruth = np.array(res_dict["candidates"])
                tvd = total_variation_dist(1 / groundtruth, prob)
                tvd_result.append(tvd)
        else:
            print("Results Not Exist!!!")
    return tvd_result


def eval_K(data, k_list, l, w):
    uniform = []
    weighted_uniform = []
    approx_degree = []
    exact_degree = []
    for k in k_list:
        filename = f'k_{k}_L_{l}_w_{w}'
        result = get_variation_dist(data, filename)
        uniform.append(result[0])
        weighted_uniform.append(result[1])
        approx_degree.append(result[2])
        exact_degree.append(result[3])
    plt.title(data)
    plt.plot(k_list, uniform, 'x-', color='r', label="uniform")
    plt.plot(k_list, weighted_uniform, 'o-', color='g', label="weighted_uniform")
    plt.plot(k_list, approx_degree, '*-', color='b', label="approx_degree")
    plt.plot(k_list, exact_degree, 's-', color='y', label="exact_degree")
    plt.xlabel("Value of parameter k of LSH")
    plt.ylabel("Statistical Distance")
    plt.legend(loc="best")
    plt.show()


def eval_L(data, k, l_list, w):
    uniform = []
    weighted_uniform = []
    approx_degree = []
    exact_degree = []
    for l in l_list:
        filename = f'k_{k}_L_{l}_w_{w}'
        result = get_variation_dist(data, filename)
        uniform.append(result[0])
        weighted_uniform.append(result[1])
        approx_degree.append(result[2])
        exact_degree.append(result[3])
    plt.title(data)
    plt.plot(l_list, uniform, 'x-', color='r', label="uniform")
    plt.plot(l_list, weighted_uniform, 'o-', color='g', label="weighted_uniform")
    plt.plot(l_list, approx_degree, '*-', color='b', label="approx_degree")
    plt.plot(l_list, exact_degree, 's-', color='y', label="exact_degree")
    plt.xlabel("Value of parameter L of LSH")
    plt.ylabel("Statistical Distance")
    plt.legend(loc="best")
    plt.show()


if __name__ == "__main__":
    dataset = "glove-100-angular"
    K_list = [11, 12, 13, 14, 15]
    L_list = [100, 200, 300]
    K = 15
    L = 100
    W = 15.7

    # eval_K(dataset, K_list, L, W)
    eval_L(dataset, K, L_list, W)
