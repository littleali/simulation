import numpy as np
import StringIO
import os
import ConfigParser

def read_and_sort(filename):
	unsorted_list = np.loadtxt(filename)
	sorted_list = np.sort(unsorted_list)
	base = sorted_list[0]
	for i in range (len(sorted_list)):
		sorted_list[i] = sorted_list[i] - base
	return sorted_list

def read_paramenter(paramenter_name):
	config = StringIO.StringIO()
	config.write(open('config.properties').read())
	config.seek(0, os.SEEK_SET)
	cp = ConfigParser.ConfigParser()
	cp.readfp(config)
	return cp.get('all', paramenter_name)


#test for read_parameter
print read_paramenter("floors.parameter")