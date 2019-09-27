from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    ret = []
    m = len(points)
    sum_of_vector = [0] * m
    for i in points:
        sum_of_vector = [v_i + w_i for v_i, w_i in zip(sum_of_vector, i)]
    for j in sum_of_vector:
        ret.append(j/m)
    return ret


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    centers = []
    m = len(data_set)
    ret = defaultdict(list)
    for i in range(m):
        ret[assignments[i]].append(data_set[i])
    for j in ret.keys():
        centers.append(point_avg(ret[j]))
    return centers


def assign_points(data_points, centers):
    """
    assign points to each cluster
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    dimension = len(a)
    point_distance = 0
    for i in range(dimension):
        point_distance = point_distance + (float(a[i]) - float(b[i]))**2
    return point_distance


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(data_set, k)


def get_list_from_dataset_file(dataset_file):

    """
    :param dataset_file: get data from dataset
    :return: a list of data
    """

    with open(dataset_file,'r') as f:
        data = csv.reader(f)
        return [list(map(int, point)) for point in data]


def cost_function(clustering:defaultdict):
    """
    :param clustering: calculate the cost function
    :return:
    """
    cost = 0
    for points in clustering.keys():
        center = point_avg(clustering[points])
        for point in clustering[points]:
            cost = cost + distance(center, point)
    return cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
