import os
import argparse
import pickle
import time
from datasets import get_dataset
from lsh import LSHBuilder, E2LSH


def get_result_fn(dataset, query_type, rep):
    if not os.path.exists(os.path.join("results", dataset, query_type)):
        os.makedirs(os.path.join("results", dataset, query_type))
    return os.path.join(os.path.join("results", dataset, query_type, rep + ".pickle"))


def run_single_exp(dataset, distance_threshold, k, L, w, validate, runs):
    data, queries, _, _ = get_dataset(dataset)
    print(f"data: {len(data)}")
    print(f"queries: {len(queries)}")

    lsh = LSHBuilder.build(len(data[0]), distance_threshold, k, L, w, validate)

    print("Building index...")
    lsh.preprocess(data)

    candidates = lsh.get_query_size(queries)

    for method in LSHBuilder.methods:
        print(f"Running (k={k}, L={L}) with {method}")
        start = time.time()
        res = LSHBuilder.invoke(lsh, method, queries, runs)
        end = time.time()
        print(f"Run finished in {end - start}s.")

        res_fn = get_result_fn(dataset, method, repr(lsh))

        res_dict = {
            "name": str(lsh),
            "method": method,
            "res": res,
            "dataset": dataset,
            "dist_threshold": distance_threshold,
            "candidates": candidates,
            "time": end - start
        }

        with open(res_fn, 'wb') as f:
            pickle.dump(res_dict, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        default="glove-100-angular",
    )
    parser.add_argument(
        '-k',
        default=15,
        type=int,
    )
    parser.add_argument(
        '-L',
        default=300,
        type=int
    )
    parser.add_argument(
        '-w',
        default=15.7,
        type=float
    )
    parser.add_argument(
        '--distance-threshold',
        default=4.7,
        type=float,
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=100,
    )
    parser.add_argument(
        '--validate',
        action='store_true',
    )

    args = parser.parse_args()
    run_single_exp(args.dataset, args.distance_threshold, args.k, args.L, args.w, args.validate, args.runs)

