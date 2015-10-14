import csv


def write_csv(data, labels, out_file_path):
    with open(out_file_path, 'a') as f:
        csv_writer = csv.writer(f)

        for i in range(0, len(data)):
            csv_writer.writerow([labels[i], data[i]])
