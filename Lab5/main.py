import os
import time
from datasets import get_dataset
from lsh import LSH


def get_result_fn(dataset, query_type, rep):
    if not os.path.exists(os.path.join("results", dataset, query_type)):
        os.makedirs(os.path.join("results", dataset, query_type))
    return os.path.join(os.path.join("results", dataset, query_type, rep + ".pickle"))


def run_single_exp(dataset, distance_threshold, k, L, w, runs):
    data, queries, _, _ = get_dataset(dataset)
    print(f"data: {len(data)}")
    print(f"queries: {len(queries)}")

    lsh = LSH(k, L, w, len(data[0]), distance_threshold)

    print("Building index...")
    lsh.preprocess(data)

    candidates = lsh.get_query_size(queries)

    for method in lsh.get_methods():
        print(f"Running (k={k}, L={L}) with {method}")
        start = time.time()
        res = lsh.invoke(method, queries, runs, cached=True)
        end = time.time()
        print(f"Run finished in {end - start}s.")

        # res_fn = get_result_fn(dataset, method, repr(lsh))

        res_dict = {
            "name": str(lsh),
            "method": method,
            "res": res,
            "dataset": dataset,
            "dist_threshold": distance_threshold,
            "candidates": candidates,
            "time": end - start
        }

        print(res_dict)

        # with open(res_fn, 'wb') as f:
        #     pickle.dump(res_dict, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    dataset = "glove-100-angular"
    K = 15
    L = 100
    W = 15.7
    R = 4.7
    runs = 1

    run_single_exp(dataset, R, K, L, W, runs)

