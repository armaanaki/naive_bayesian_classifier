#!/usr/bin/python

# Course: CS4267
# Student name: Armaan Esfahani 
# Student ID: 000764818
# Assignment #: #2
# Due Date: October 2, 2019
# Signature: A.E. 
# Score: _________________

# imports for our progam
import csv
import random
import math
import argparse


# method to load data from a dataset and split it data to use and data for  comparison
# compare_set: array used as training data (where the data set comapres against), defaults to a null array if none is set
# data_set: array of data to test against the compare_set (what our program will try to predict), defaults to null array if none is set
# split_amount: the fraction that our data will split into (how much of the data set goes into each array), defaults to 80% if none is set
# filename: File location of dataset to load, defaults to the iris data set if none is set
def load_data(compare_set, data_set, split_amount, filename):
    # open the file in read-only as a csv
    with open(filename, 'r') as csvfile:
        # load the csv into a list
        reader = csv.reader(csvfile)
        data = list(reader)

        # iterate all values from csv
        for index in range(len(data)-1):
            # set all numerical values to floats so they can be manipulated later
            for x in range(len(data[index]) - 1):
                data[index][x] = float(data[index][x])

            # roll a random number, if it is below the split amount add it to compare set, otherwise it goes to the data set
            if random.random() < split_amount:
                compare_set.append(data[index])
            else:
                data_set.append(data[index])

# function that returns an array with each class and the mean and std of each variable
def class_array(array, rounding):
    sort_array = {}
    
    # add all the points to their classifier
    for x in array:
        if (x[-1] not in sort_array):
            sort_array[x[-1]] = []
        sort_array[x.pop()].append(x)

    mean_array = {}

    # add each element to an array corresponding to it's position then calculate the mean
    for classifier in sort_array:
        total_attributes =  len(sort_array[classifier][0])
        mean = [0.0] * total_attributes
        mean_array[classifier] = []
        
        for point in sort_array[classifier]:
            for x in range(total_attributes):
                mean[x] += point[x]

        for x in range(len(mean)):
            mean[x] = round(mean[x] / len(sort_array[classifier]), rounding)

        mean_array[classifier].append(mean)

    std_array = {}

    # use the mean to find the standard deviation
    for classifier in mean_array:
        index = 0
        std = [0.0] * len(sort_array[classifier][0])
        std_array[classifier] = []

        for mean in mean_array[classifier][0]:
            for x in sort_array[classifier][:]:
                    std[index] += pow(x[index] - mean, 2)

            std[index] = round(math.sqrt(std[index] / (len(sort_array[classifier]) - 1) ), rounding)
            index += 1

        std_array[classifier].append(std)

    class_array = {}

    # combine mean and standard deviation, then return it as an array
    for classifier in mean_array:
        class_array[classifier] = []
        for x in range(len(mean_array[classifier][0])):
            class_array[classifier].append([mean_array[classifier][0][x], std_array[classifier][0][x]])

    return class_array

# main function that holds the logic for printing guesses and accuracy
def main(filename, split, rounding):
    # variables used throughout function
    compare_set = []
    data_set = []
    correct = 0
    incorrect = 0

    # load data into our variables
    load_data(compare_set, data_set, split, filename)

    sort_array = class_array(data_set, rounding)
    print(sort_array)


# parser arguments to make running the program easier
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="the location of the data file (defaults to iris.data)")
parser.add_argument("-s", "--split", help="the amount of the dataset to be split into training data (the rest is used as guessing points, defaults to 0.8)")
parser.add_argument("-r", "--round", help="number of decimals to round to (defaults to 1)")
args = parser.parse_args()

# use filename if filename was provided
if args.filename:
    filename = args.filename
else:
    filename = "iris.data"

# use split if split was provided, exit if it does not fall between 1 and 0
if args.split:
    split = float(args.split)
    if split <= 0:
        print("split may not be 0 or less!")
        exit(1)
    if split >= 1:
        print("split may not be 1 or more!")
        exit(1)
else:
    split = 0.8

if args.round:
    rounding = int(args.round)
else:
    rounding = 1

main(filename, split, rounding)
