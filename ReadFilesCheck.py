# Module imports
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Path generation
path = os.getcwd()
path_lib = os.path.join(path, 'lib')
path_out = os.path.join(path, 'out_old')
filenames = os.listdir(path_out)


# Functions
def size_check(input_mat, x_in, y_in):
    check_out = True
    dim = input_mat.shape
    if (dim[0] > x_in) or (dim[1] > y_in):
        check_out = False
    return check_out


def identical_check(input_mat, check_mat):
    check_out = True
    out_temp = "Mat1: \t" + str(input_mat[20, 189]) + "\tMat 2: \t" + str(check_mat[20, 189])
    print(out_temp)
    dim = input_mat.shape
    for i in range(dim[0]-1):
        for j in range(dim[1]):
            if input_mat[i, j] != check_mat[i, j]:
                check_out = False
    return check_out


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


# Variable decleration
x = 304
y = 246
mat = np.zeros((len(filenames)-1, x, y))
string_mat = np.zeros([x, y]).astype(str)
check = np.zeros(len(filenames)-1)
outtext = ""
j = 0

# File name check
for i in range(len(filenames) - 1):
    # print(filenames[i])
    name = filenames[i]
    file_temp = pd.read_csv(os.path.join(path_out, filenames[i]))
    # print(file_temp[20, 189])
    dim = file_temp.shape
    if dim[0] != x or dim[1] != y:
        file_temp = delete_extra(file_temp, x, y)
    if filenames[i].__contains__("Station_Location"):
        file_temp = file_temp.astype(str)
        string_mat[:x, :y] = file_temp
        j = j - 1
    else:
        mat[j, :x, :y] = file_temp
        plt.imshow(mat[i], cmap='hot', interpolation='nearest')
    check[i] = size_check(file_temp, x, y)
    j = j + 1
    plt.show()

outtext = "\n" + filenames[0] + " is the base comparison\n"
print(outtext)
for i in range(1, len(filenames) - 1):
    outtext = filenames[i] + " is a copy:\t\t"
    outtext = outtext + str(identical_check(mat[0, :x, :y], mat[i, :x, :y])) + "\n"
    print(outtext)

