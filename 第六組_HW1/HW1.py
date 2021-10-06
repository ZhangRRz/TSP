import csv
from itertools import permutations
from numpy.linalg import norm
import math
import matplotlib.pyplot as plt
import time
import multiprocessing

# Find TSP using brute-force
# Getting the data
data = []
with open('readfile.txt', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        x = int(row[0].split(" ")[1])
        y = int(row[0].split(" ")[2])
        # Storing the point as this: [(x1,y1), (x2,y2), ...]
        data.append((x, y))
point_number = dict()

# Record the point coordinates as to their number.
for i, d in enumerate(data):
    point_number[d] = i

# Removing the first point in the list. (To anchor the starting point.)
starting_point = data[0]
data.pop(0)

min_dist = float("inf")
winning_permutaion = []
start_time = time.time()


def calc(data: list, second_point: tuple, first_point: tuple, process_num: int, winning_permutaion_dict, min_dist_dict):
    min_dist = float("inf")
    inidist = math.sqrt(math.pow(
        (second_point[0]-first_point[0]), 2)+math.pow((second_point[1]-first_point[1]), 2))
    # Calculate execute time(main function)
    for c in permutations(data, len(data)):
        dist = math.sqrt(math.pow(
            second_point[0]-c[0][0], 2) + math.pow(second_point[1]-c[0][1], 2)) + inidist
        for i, d in enumerate(c):
            if(i == len(c)-1):
                break
            dist += math.sqrt(math.pow(d[0]-c[i+1]
                                       [0], 2)+math.pow(d[1]-c[i+1][1], 2))
        dist += math.sqrt(math.pow(c[-1][0]-first_point[0],
                                   2)+math.pow(c[-1][1]-first_point[1], 2))
        if(dist < min_dist):
            min_dist = dist
            winning_permutaion = c
    initial_list = [first_point, second_point]
    for x in winning_permutaion:
        initial_list.append(x)
    winning_permutaion_dict[process_num] = initial_list
    min_dist_dict[process_num] = min_dist


# multithread
if __name__ == '__main__':
    manager = multiprocessing.Manager()
    winning_permutaion_dict = manager.dict()
    min_dist_dict = manager.dict()
    processes = []
    for i, dt in enumerate(data):
        sp = dt
        n = [x for x in data if x != dt]
        p = multiprocessing.Process(target=calc, args=(
            n, sp, starting_point, i, winning_permutaion_dict, min_dist_dict))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    ans = []
    plot_x = []
    plot_y = []

    # get the key of the minimun distance in processes
    process_key = min(min_dist_dict, key=min_dist_dict.get)
    execution_time = time.time() - start_time

    for i in winning_permutaion_dict[process_key]:
        ans.append(point_number[i]+1)
        plot_x.append(i[0])
        plot_y.append(i[1])

    plot_x.append(starting_point[0])
    plot_y.append(starting_point[1])

    with open('output.txt', 'w') as f:
        f.write("Best Visit Order: " + str(ans) + "\n")
        f.write("Best(Shortest) Distance: " +
                str(min_dist_dict[process_key]) + "\n")
        f.write("Execution time: " + str(execution_time) + "\n")

    # Draw the shortest path
    plt.plot(plot_x, plot_y)
    plt.scatter(plot_x, plot_y, color='coral')
    plt.title("TSP Best(Shortest) Path")
    plt.xlabel("x")
    plt.ylabel("y", rotation=0)
    plt.savefig("TSP.png")
