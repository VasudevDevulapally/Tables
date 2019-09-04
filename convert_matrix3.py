#!/usr/bin/python3

import argparse
import os
import re
import sys
import csv
import pandas as pd 

def apply_threshold(i, t):
    """
        Return i if i>t else 0

        Parameters:
          i - value to test [float]
          t - threshold [float]
    """
    if abs(i)>t:
        return i
    else:
        return 0.0

def read_matrix_from_file(matrix_file, threshold):
    """
        Read the matrix from the input file

        Values <=threshold are set to 0
    """
    matrix = []
    with open(matrix_file) as infile:
        for line in infile:
            if(line != "\n"):
                row = line.strip() #.split(sep)
                row_values = re.compile(",").split(row)
                row_values = list(map(float, row_values))

                for i in range(len(row_values)):
                    row_values[i] = apply_threshold(row_values[i], threshold)

                matrix.append(row_values) 
               
    return matrix

def read_positions_from_file(positions_file):
    """
        Read the matrix from the input file

        Values <=threshold are set to 0
    """
    positions = []
    with open(positions_file) as infile:
        for line in infile:
            if(line.rstrip()):
                row = line.strip() #.split(sep)
                row_values = re.compile("\s+").split(row)
                row_values = list(map(float, row_values))

                positions.append(row_values) 
               
    return positions

def determine_matrix_max(matrix):
    """
        Determine the max value in the matrix
        (e.g. used for normalization)
    """
    max_val = -1.0

    for row in matrix:
        for value in row:
            if value > max_val:
                max_val = value

    return max_val

def read_id_file(id_file):
    """
        Read the file containing the row/column IDs
    """
    ids = []
    with open(id_file) as infile:
        for line in infile:
            if line.rstrip() != "":
                ids.append(line.rstrip())

    return ids

def write_output_file(matrix, positions, ids, output_file, threshold, max_val, file_id,atlas):
    """
        Write tab-sep. output file - output file must be the name of the file without extension
    """
    # NOTE: appends to the file if it exists instead of overwriting!

    write_header = True
    if (os.path.isfile(output_file)):
        write_header = False

    with open(output_file, "a") as outfile:
        if (write_header):
            outfile.write("Origin_Area\tTarget_Area\tMeasured_Connection_Strength\tNormalized_Connection_Strength\tOriginx\tOriginy\tOriginz\tTargetx\tTargety\tTargetz\tPatient_ID\tAtlas\n")
        for i in range(len(ids)):
            for j in range(len(ids)):
                if(matrix[i][j]>threshold and matrix[i][j]!=0):
                    normalized_value = matrix[i][j] / max_val
                    outfile.write("%s\t%s\t%.15f\t%.15f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%s\t%s\n" % (ids[i], ids[j], matrix[i][j], normalized_value, positions[i][0], positions[i][1], positions[i][2], positions[j][0], positions[j][1], positions[j][2],file_id,atlas))

########################################################################################################################
########################################################################################################################
parser = argparse.ArgumentParser(description='''Convert matrix file to value-per-line file''',
                                 epilog="Biomax Informatics AG")

parser.add_argument('-i', metavar="<matrix file>", action='store', dest='matrix_file',
                    help='Input file containing the matrix with values', required=True)
parser.add_argument('-n', metavar="<name file>", action='store', dest='id_file',
                    help='File containing the row/column names of the matrix', required=True)
parser.add_argument('-p', metavar="<positions file>", action='store', dest='positions_file',
                    help='File containing the row/column names of the matrix', required=True)
parser.add_argument('-o', metavar="<output file>", action='store', dest='out_file',
                    help='Output file', required=True)
parser.add_argument('-id', metavar="<file id>", action='store', dest='file_id',
                    help='File ID (will be appended to the output lines!)', required=True)
parser.add_argument('-atlas', metavar="<atlas>", action='store', dest='atlas',
                    help='atlas (will be appended to the output lines!)', required=True)
parser.add_argument('-t', metavar="<float>", action='store', dest='threshold',
                    default="0.0", help='Threshold value. Values equal or lower than this will be set to 0 [default=0.0]')

parser._optionals.title = "Arguments"
params = parser.parse_args()

matrix_file = params.matrix_file
id_file = params.id_file
positions_file = params.positions_file
output_file = params.out_file
threshold = float(params.threshold)
file_id = params.file_id
atlas   = params.atlas

# check parameters
for f in [matrix_file, positions_file, id_file]:
    if not os.path.isfile(f):
        raise Exception("Input file %s does not exist!" % f)
        sys.exit(1)
##############################

ids = read_id_file(id_file)
print("Got %d ids" % len(ids))
matrix_values = read_matrix_from_file(matrix_file, threshold)
positions = read_positions_from_file(positions_file)
max_value = determine_matrix_max(matrix_values)
print("position values %d " % len(positions))
print("matrix values %d " % len(matrix_values))
write_output_file(matrix_values, positions, ids, output_file, threshold, max_value, file_id,atlas)


