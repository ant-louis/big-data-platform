import csv
import sys
 

def split_csv(filename):
    """
    Split the csv file 'bts-data-alarm-2017' into multiple
    sub-files according to their station_id.
    """
    with open(filename, mode='r') as csv_file:
        # Read csv file and store headers
        csv_reader = csv.DictReader(csv_file)
        headers = csv_reader.fieldnames

        # Sort the database by station_id
        csv_reader = sorted(csv_reader, key=lambda row: float(row['station_id']))

        # Init variables
        curr_sid = None  # current station_id
        counter_sid = 0  # Number of different station_id
        output_file = None  # output file

        # Split into sub-files
        for row in csv_reader:
            # If the station_id change
            if row['station_id'] != curr_sid:
                # Update current station id
                curr_sid = row['station_id']

                # Close the previous outfile (except for first pass)
                if output_file:
                    output_file.close()
                
                # Generate a subset name
                file_name = '../../data/subdatasets/subdataset_' + str(counter_sid) + '.csv'
                counter_sid += 1

                # Create the file
                output_file = open(file_name, mode='w')
                writer = csv.DictWriter(output_file, fieldnames=headers)
                writer.writeheader()
                print("Start writing subdataset number {}...".format(counter_sid))
            
            # Write current row
            writer.writerow(row)
        
        # Close the file
        output_file.close()


if __name__ == "__main__":
    filename = '../../data/bts-data-alarm-2017.csv'
    split_csv(filename)
