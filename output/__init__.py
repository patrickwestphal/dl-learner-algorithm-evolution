import matplotlib.pyplot as plt


# TODO: CSV output

def plot(data, labels, out_file_path):
    num_vals = data.shape[0]
    x = range(num_vals)
    plt.plot(x, data)
    # plt.xticks(x, labels, rotation=45, ha='right')
    plt.xticks(x, labels, rotation='vertical')
    plt.tight_layout()
    plt.savefig(out_file_path)

