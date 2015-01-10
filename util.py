import numpy as np
import StringIO
import os
import ConfigParser
from time import gmtime, strftime
import time


def read_and_sort(filename):
	unsorted_list = np.loadtxt(filename)
	sorted_list = np.sort(unsorted_list)
	base = sorted_list[0]
	for i in range (len(sorted_list)):
		sorted_list[i] = sorted_list[i] - base
	return sorted_list

def read_parameter(paramenter_name):
	config = StringIO.StringIO()
	config.write(open('config.properties').read())
	config.seek(0, os.SEEK_SET)
	cp = ConfigParser.ConfigParser()
	cp.readfp(config)
	return cp.get('all', paramenter_name)

def log(string):
    print time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + ": " + str(string)










#test for read_parameter
# print util.read_parameter("floors.parameter")