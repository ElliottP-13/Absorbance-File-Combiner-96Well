import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import math

path_to_files = 'Data/'


def parse_filename(name):
    info = {}
    info['filename'] = name

    # name manipulation
    name = name.replace('.xlsx', '')  # removes xlsx from end of file name
    parse = name.split(' ')

    info['organism'] = parse[0]  # first thing in filename
    info['plate'] = parse[1]  # plate type (2nd thing)
    t = parse[2].split('.')  # the time, split on .
    info['time'] = t[0] + ':' + t[1]  # writes hh:mm
    d = parse[3].split('.')  # The date, split on .
    info['date'] = d[0] + '/' + d[1]  # writes mm/dd

    return info


# Maps the flattened index to Letter Number (F10) to match output from absorbance reader
def map_indx_to_coord(indx):
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = [str(i + 1) for i in range(12)]

    row = math.floor(indx/len(cols))
    column = indx % len(cols)

    return rows[row] + cols[column]


# Reads the raw data from the excel file
# Assumes matrix data is in C25-N32 in excel
# Prefix is Prepended onto each label in dictionary
def read_file(file, prefx):
    df = pd.read_excel(file, header=23, engine='openpyxl')
    raw = df.to_numpy()
    data = np.delete(raw, [-1, 0,1], 1)
    # remove -1, removes the last value (590) which is the wavelength
    # remove 0 removes blank column
    # remove 1 removes row labels A-H

    # Shape of data should be (9, 12). 9 row by 12 col
    plates = data.flatten()

    info = {}
    for i in range(len(plates)):
        info[prefx + map_indx_to_coord(i)] = plates[i]

    return info


# Reads and parses all the filenames within a directory
def get_all_info(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]  # stole from internet. Gets all the filenames within a folder
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

    all_info = [parse_filename(file) for file in onlyfiles]

    return all_info


# Combines all the files for the given organism
# Expects the relevant files to be under path_to_files in a folder labeled with organism name
def main(organism):
    path = path_to_files + organism + '/'
    all_info = get_all_info(path)

    dates = set([d['date'] for d in all_info])  # gets a set of all the dates

    dataframe = []

    for day in dates:  # iterate through each date

        # find the 2 different plate types for the date
        p1, p2 = None, None

        for d in all_info:
            if d['date'] == day and d['plate'] == 'PM1':
                p1 = d
            elif d['date'] == day and d['plate'] == 'PM2A':
                p2 = d

        # Check for missing days
        if p1 is None or p2 is None:  # if missing a datapoint, skip it
            continue

        # now we need to merge p1, p2
        data1 = read_file(path + p1['filename'], 'PM1 ')
        data2 = read_file(path + p2['filename'], 'PM2A ')

        # day_info = {**p2, **data2}  # For running with only half data (no PM1 plate)
        day_info = {**p1, **data1, **data2}  # Merge the dictionaries returned
        # p1 gives info on time, date, organism, etc
        # data1/2 give the relevent cells from the matrix in each file
        day_info.pop('filename')  # just removes filename from the dictionary

        dataframe.append(day_info)

    dataframe = pd.DataFrame(dataframe)
    dataframe.to_csv(path_to_files + '/results/' + organism + '.csv')  # save as a csv

    '''
    This code is if you export directly into excel
    You will have to select the time and date columns in excel to format this into anything human-readable
    '''

    # Set the format to date/time for excel
    dataframe['time'] = pd.to_datetime(dataframe['time'], format="%H:%M")
    dataframe['date'] = pd.to_datetime(dataframe['date'], format="%m/%d")

    dataframe.to_excel(path_to_files + '/results/' + organism + '.xlsx')  # save as Excel


'''  CHANGE DOWN HERE!! '''

main('PL20H PM Plate')
