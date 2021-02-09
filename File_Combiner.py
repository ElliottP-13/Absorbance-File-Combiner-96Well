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

def map_indx_to_coord(indx):
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = [str(i + 1) for i in range(12)]

    row = math.floor(indx/len(cols))
    column = indx % len(cols)

    return rows[row] + cols[column]


def read_file(file, prefx):
    df = pd.read_excel(file, header=23, engine='openpyxl')
    raw = df.to_numpy()
    data = np.delete(raw, [-1, 0,1], 1)
    # Shape of data should be (9, 12). 9 row by 12 col
    plates = data.flatten()

    info = {}
    for i in range(len(plates)):
        info[prefx + map_indx_to_coord(i)] = plates[i]

    return info


# Main function
# Tells the rest of the program what files to read and combines results
def read_organism(name):
    output_f = open(path_to_files + 'results_' + name + '.csv', 'a')
    for day in range(1, 30):
        file_a = path_to_files + name + '-' + str(day) + '-A.xpt'
        file_b = path_to_files + name + '-' + str(day) + '-B.xpt'
        data = combine_plates(file_a, file_b)

        sb = ''
        for x in data:  # turns numpy array into csv string
            sb += str(x) + ','
        sb = sb[:-1]  # remove final comma
        output_f.write(sb + '\n')
    output_f.close()



def get_all_info(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]  # stole from internet. Gets all the filenames within a folder
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

    all_info = [parse_filename(file) for file in onlyfiles]

    return all_info



def main(organism):
    path = path_to_files + organism + '/'
    all_info = get_all_info(path)

    dates = set([d['date'] for d in all_info])  # gets a set of all the dates

    dataframe = []

    for day in dates:
        p1, p2 = None, None

        for d in all_info:
            if d['date'] == day and d['plate'] == 'PM1':
                p1 = d
            elif d['date'] == day and d['plate'] == 'PM2A':
                p2 = d


        # now we need to merge p1, p2
        data1 = read_file(path + p1['filename'], 'PM1 ')
        data2 = read_file(path + p2['filename'], 'PM2A ')

        day_info = {**p1, **data1, **data2}
        day_info.pop('filename')  # just removes filename from the dictionary

        dataframe.append(day_info)

    dataframe = pd.DataFrame(dataframe)
    dataframe.to_csv(path_to_files + '/results/' + organism + '.csv')  # save as a csv

    '''
    This code is if you export directly into excel
    You will have to select the time and date columns in excel to format this into anything human-readable
    '''

    # Set the format to date/time for excel
    # dataframe['time'] = pd.to_datetime(dataframe['time'], format="%H:%M")
    # dataframe['date'] = pd.to_datetime(dataframe['date'], format="%m/%d")

    # dataframe.to_excel(path_to_files + '/results/' + organism + '.xlsx')  # save as Excel




main('CG23.4 PM Plates')