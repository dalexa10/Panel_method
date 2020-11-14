import matplotlib.pyplot as plt

def plot_scatter(X, Y, x_start, x_end, y_start, y_end, color='r'):
    width = 10.0
    height = (y_end - y_start) / (x_end - x_start) * width
    plt.figure(figsize=(width, height))
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.xlim(x_start, x_end)
    plt.ylim(y_start, y_end)
    plt.scatter(X, Y, s=5, color=color, marker='o')
    scatter_graph = plt.show()
    return scatter_graph