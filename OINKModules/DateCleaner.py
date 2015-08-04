from __future__ import division
import math, os, sys, datetime
from PyQt4 import QtGui, QtCore
import pandas

def main():
	print "Date Cleaner application"
	input_file = "input.csv"
	input_data_frame = pandas.DataFrame.from_csv(input_file,header=0)
	print input_data_frame["Update_timestamp"]
if __name__ == "__main__":
	main()