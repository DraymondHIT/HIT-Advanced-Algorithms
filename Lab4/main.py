from graph import Graph
from timeit import default_timer as timer


def main():
    n_list = [16, 32, 64, 128, 256, 512, 1024]
    times_list = [200, 150, 100, 80, 60, 40, 20]
    weight_list = []
    time_list = []

    for i in range(len(n_list)):
        weights = 0
        tic = timer()
        for j in range(times_list[i]):
            graph = Graph(n_list[i])
            weight, _ = graph.prim()
            weights += weight
        toc = timer()
        weight_list.append(weights / times_list[i])
        time_list.append((toc - tic) / times_list[i])

    print(weight_list)
    print(time_list)


if __name__ == "__main__":
    main()
