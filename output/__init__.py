import matplotlib.pyplot as plt


def plot(data, labels, out_file_path):
    # TODO: reverse data and labels
    num_vals = data.shape[0]
    x = range(num_vals)
    plt.plot(x, data)
    plt.xticks(x, labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(out_file_path)

