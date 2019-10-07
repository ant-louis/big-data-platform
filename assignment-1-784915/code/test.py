import csv

if __name__ == "__main__":

    path = '../data/googleplaystore.csv'
    
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(row)
                line_count += 1
            if line_count==10:
                break
        
