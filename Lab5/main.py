import os
import argparse
import pickle
import time
from datasets import get_dataset
from lsh import LSHBuilder, E2LSH
from distance import l2, jaccard


def get_result_fn(dataset, query_type, rep):
    if not os.path.exists(os.path.join("results", dataset, query_type)):
        os.makedirs(os.path.join("results", dataset, query_type))
    return os.path.join(os.path.join("results", dataset, query_type, rep + ".pickle"))


def run_single_exp(dataset, distance_threshold, lsh_method, k, L, w, validate, report_output, runs):
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
        print(f"Run finished in {time.time() - start}s.")

        res_fn = get_result_fn(dataset, method, repr(lsh))

        res_dict = {
            "name": str(lsh),
            "method": method,
            "res": res,
            "dataset": dataset,
            "dist_threshold": distance_threshold,
            "candidates": candidates,
        }

        print(res_dict)

        with open(res_fn, 'wb') as f:
            pickle.dump(res_dict, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        default="mnist-784-euclidean",
    )
    parser.add_argument(
        '-k',
        default=15,
        type=int,
    )
    parser.add_argument(
        '-L',
        default=100,
        type=int
    )
    parser.add_argument(
        '-w',
        default=3.1,
        type=float
    )
    parser.add_argument(
        '--distance-threshold',
        default=5,
        type=float,
    )
    parser.add_argument(
        '--method',
        type=str,
        required=False,
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=5,
    )

    parser.add_argument(
        '--report-output',
        action='store_true',
    )

    parser.add_argument(
        '--validate',
        action='store_true',
    )

    args = parser.parse_args()

    run_single_exp(args.dataset, args.distance_threshold, args.method,
                   args.k, args.L, args.w, args.validate, args.report_output, args.runs)

