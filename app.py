"""
The purpose of this program is to fix the datetime of results from the gasmet
machine.

Author: Hayden Elza
Email: hayden.elza@gmail.com
Created: 2017-10-25
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os
from shutil import copyfile

# Use the first observation of each to sync the times
# The licor time will be used as the "true" time
licor_time = "2017-10-24 06:45:05"
gasmet_time = "2009-10-23 14:38:07"

#----------

# Get time difference
ltime = datetime.strptime(licor_time, "%Y-%m-%d %H:%M:%S")
gtime = datetime.strptime(gasmet_time, "%Y-%m-%d %H:%M:%S")
time_diff = ltime-gtime


def adjust_datetime(gasmet_table_path, output_path):
	# Read gasmet data to dataframe
	gasmet_table = pd.read_table(gasmet_table_path, "\t")

	# Adjust time
	gasmet_table['Date'] = gasmet_table['Date'].apply(lambda x: str(datetime.strptime(x, "%Y-%m-%d %H:%M:%S") + time_diff))

	# Write dataframe to file
	gasmet_table.to_csv(output_path, sep='\t', index=False)

def trim_data(gasmet_table_path,output_path):
	# Make copy of orginal file
	copyfile(gasmet_table_path, os.path.join(os.path.dirname(gasmet_table_path), "Results_original.txt"))

	# Trim keeping only last run
	header = "Date\tWater vapor H2O (vol-%)\tResidual\tCarbon dioxide CO2 (ppm)\tResidual\tMethane CH4 (ppm)\tResidual\tNitrous oxide N2O (ppm)\tResidual\tAmmonia NH3 (ppm)\tResidual\tCarbon monoxide CO (ppm)\tResidual\tAmbient pressure (mbar)\tResidual\tInterferometer temperature (\xb0C)\tResidual\tDetector temperature (-\xb0C)\tResidual\tIFG peak height (V)\tResidual\tIFG Center ()\tResidual\tSpectrum file\tLibrary file"
	with open(gasmet_table_path, "r") as file: lines = file.read().split(header)
	with open(output_path, "w") as file: file.write(header + str(lines[-1]))


# Iterate through input directory
for directory in os.listdir("input/"):

	# Build gasmet table path
	gasmet_table_path = os.path.join("input/", directory, "Results/Results.txt")

	# Build output path
	output_path = os.path.join("output/", directory + ".txt")

	# Check if path exists first
	if os.path.isfile(gasmet_table_path): 

		# Trim data
		trim_data(gasmet_table_path,gasmet_table_path)

		# Adjust time and place new results in output
		adjust_datetime(gasmet_table_path, output_path)
