import os
import matplotlib.pyplot as plt

def save_plot(plt, filename):
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, filename)
    plt.savefig(filepath)
    plt.show()
