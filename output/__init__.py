import csv

# import matplotlib.pyplot as plt

# TODO: CSV output

def plot(data, labels, out_file_path):
    num_vals = data.shape[0]
    x = range(num_vals)
    # plt.plot(x, data)
    # plt.xticks(x, labels, rotation=45, ha='right')
    # plt.xticks(x, labels, rotation='vertical')
    # plt.tight_layout()
    # plt.savefig(out_file_path)


def write_csv(data, labels, out_file_path):
    with open(out_file_path, 'a') as f:
        csv_writer = csv.writer(f)

        for i in range(0, len(data)):
            csv_writer.writerow([labels[i]] + data[i])