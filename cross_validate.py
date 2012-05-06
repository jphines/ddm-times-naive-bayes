import csv
import numpy
from numpy import matrix
import math
import matplotlib.pyplot as plt
import sys


def load_data():
    reader = csv.reader(open("polyfit.tsv", "rb"), delimiter='	')
    reader.next()
    xmat = numpy.asmatrix(numpy.ones((200, 1)))
    ymat = numpy.asmatrix(numpy.ones((200, 1)))
    count = 0
    for x, y in reader:
        xmat[count] = float(x)
        ymat[count] = float(y)
        count += 1
    return [xmat, ymat]


def best_fit(xmat, ymat):
    return ((xmat.T) * xmat).I * xmat.T * ymat


def k_dimensionify(xmat, k):
    size = xmat.shape[0]
    karr = numpy.asmatrix(numpy.ones((size, k + 1)))
    count = 0
    while count < size:
        x = xmat[count]
        kcount = 0
        while kcount <= k:
            if(k == 0):
                karr[count] = x ** kcount
            else:
                karr[count, kcount] = x ** kcount
            kcount += 1
        count += 1
    return karr


def mean_error(xmat, ymat, func):
    count = 0
    kcount = 0
    error = 0
    size = xmat.shape[1]
    k = func.shape[0]
    while count < size:
        x = xmat[size]
        y = ymat[size]
        y1 = 0
        while kcount < k:
            y1 += func[kcount] * (x ** kcount)
            kcount += 1
        kcount = 0
        error += math.sqrt((y - y1) ** 2)
        count += 1
    return error / count


def cross_validate(xmat, ymat, dimensions):
    stacked = numpy.hstack((xmat, ymat))
    #numpy.random.shuffle(stacked)
    array = numpy.vsplit(stacked, 2)
    training_set = numpy.hsplit(array[0], 2)
    testing_set = numpy.hsplit(array[1], 2)
    train_x = training_set[0]
    train_y = training_set[1]
    test_x = testing_set[0]
    test_y = testing_set[1]
    count = 0
    testoverall = 0
    trainoverall = 0
    test_array = numpy.ones(dimensions)
    train_array = numpy.ones(dimensions)
    best_fit_funcs_array = []
    while count < dimensions:
        print "Calculating dimension: " + str(count)
        best_fit_func = best_fit(k_dimensionify(train_x, count), train_y)
        test = mean_error(test_x, test_y, best_fit_func)
        train = mean_error(train_x, train_y, best_fit_func)
        print "Test  Mean Error: " + str(test)
        print "Train Mean Error: " + str(train)
        test_array[count] = test
        train_array[count] = train
        best_fit_funcs_array.append(best_fit_func)
        count += 1
        testoverall += test
        trainoverall += train
    test_min = test_array.argmin(axis=0)
    best_fit_func = best_fit_funcs_array[test_min]
    return [test_array, train_array, best_fit_func]


def plot_mins(testarr, trainarr, dimens):
    t = numpy.arange(0., dimens, 1.)
    plt.plot(t, testarr, 'r--', t, trainarr, 'bs')
    plt.show()
    sys.exit(1)



def plot_scatter(arrays, best_func):
    plt.show()

if __name__ == "__main__":
    dimensions = 20
    arrays = load_data()
    crossed = cross_validate(arrays[0], arrays[1], dimensions)
    print crossed[2]
    plot_mins(crossed[0], crossed[1], dimensions)
    #plot_scatter(arrays, crossed[2])
