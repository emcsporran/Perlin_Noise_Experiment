# Module imports
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from perlin_noise import PerlinNoise
import seaborn as sns


def get_min(input_mat):
    mat_min = 0
    dim = input_mat.shape
    for i in range(dim[0] - 1):
        for j in range(dim[1]):
            if input_mat[i, j] <= mat_min:
                mat_min = input_mat[i, j]
    return mat_min


def get_max(input_mat):
    mat_max = 0
    dim = input_mat.shape
    for i in range(dim[0] - 1):
        for j in range(dim[1]):
            if input_mat[i, j] >= mat_max:
                mat_max = input_mat[i, j]
    return mat_max


def normalize(input_mat,dim):
    start = np.ones((dim[0], dim[1]))
    tot_min = abs(get_min(input_mat))
    tot_max = abs(get_max(input_mat))
    input_mat = (input_mat + start * tot_min) / (1.95*(tot_min + tot_max))
    print(get_min(input_mat))
    print(get_max(input_mat))
    return input_mat


def add_min(input_mat, min_in, max_in):
    input_mat = np.asarray(input_mat)
    dim = input_mat.shape
    start = np.ones((dim[0], dim[1]))
    norm_mat = normalize(input_mat,dim)
    adjusted = start*min_in + (max_in-min_in)*norm_mat
    print('adjusted')
    print(get_min(start))
    print(get_max(adjusted))
    return adjusted


def delete_extra(largemat, x_in, y_in):
    dim = largemat.shape
    delta = [0, 0]
    delta[0] = dim[0] - x_in
    delta[1] = dim[1] - y_in
    smallmat = largemat.to_numpy()
    if delta[0] > 0:    # Rows notation
        smallmat = np.delete(smallmat, np.s_[x_in-1:x_in+delta[0]-1], axis=0)
    if delta[1] > 0:    # Columns notation
        smallmat = np.delete(smallmat, np.s_[y_in-1:y_in+delta[1]-1], axis=1)
    return smallmat


def sum_calc(input_mat, dim):
    sum_val = 0.0
    for i in range(dim[0] - 1):
        for j in range(dim[1] - 1):
            sum_val = sum_val + np.asarray(input_mat)[i, j]
    return sum_val


x = 304
y = 246


min_temp = 0
max_temp = 3
seed_input = 540
format_type = 'int'
name = "unit_arson_report.csv"
#name = "unit_camping_traffic.csv"
#name = "unit_firework_sales.csv"
#name = "average_pop_density.csv"
#name = "average_foliage_density.csv"
#name = "average_rainfall.csv"
#name = "average_predic_temp.csv"

path = os.getcwd()
path_lib = os.path.join(path, 'lib')
path_out = os.path.join(path, 'out')

file_out = os.path.join(path_out,name)
bin_mat = pd.read_csv(os.path.join(path_lib, 'binmap.csv'))
dim = bin_mat.shape
if dim[0] != x or dim[1] != y:
    file_temp = delete_extra(bin_mat, x, y)


noise = PerlinNoise(octaves=1.5, seed=seed_input)
xpix, ypix = y, x
# pic = noise([0.5, 0.5]) == noise([0.5, 0.5, 0, 0, 0])
pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]

pic = bin_mat*(add_min(pic, min_temp, max_temp))

if format_type == 'double':
    np.savetxt(file_out, pic, fmt='%1.4f', delimiter=",")
    ax = sns.heatmap(pic, linewidth=0.5)
    plt.show()
else:
    print("The sum of the array is:")
    np.savetxt(file_out, pic, fmt='%i', delimiter=",")
    print(sum_calc(pic, dim))
    print(np.sum(np.sum(pic)))
    ax = sns.heatmap(pic.astype(int), linewidth=0.5)
    plt.show()

