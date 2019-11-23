import pandas as pd
import sys


def sort_csv(filename):
    """
    """
    df = pd.read_csv(filename, header=0, sep=',')
    df['datetime'] = pd.to_datetime(df['event_time'])
    df.sort_values(by=['datetime'], inplace=True, ascending=True)
    df.drop(columns=['datetime'], inplace=True)
    df.to_csv('../../data/sorted_bts-data-alarm-2017.csv', index=False)



def split_csv(filename):
    """
    """
    csvfilename = open(filename, 'r').readlines()

    # Store header values
    header = csvfilename[0] 

    # Remove header from list
    csvfilename.pop(0) 
    
    # Number of lines to be written in new file
    record_per_file = 10000
    count = 1

    for j in range(len(csvfilename)):
        if j % record_per_file == 0:
            write_file = csvfilename[j:j+record_per_file]
            # Adding header at the start of the write_file
            write_file.insert(0, header)
            # Write in file
            out = '../../data/subdatasets/subdataset_'
            open(str(out)+ str(count) + '.csv', 'w+').writelines(write_file)
            count += 1


if __name__ == "__main__":
    sort_csv('../../data/bts-data-alarm-2017.csv')
    split_csv('../../data/sorted_bts-data-alarm-2017.csv')