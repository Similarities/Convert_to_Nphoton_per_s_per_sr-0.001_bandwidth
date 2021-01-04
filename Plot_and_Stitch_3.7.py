import matplotlib.pyplot as plt
import numpy as np
import os


class PlotAndStitch:
    def __init__(self, path, my_files, column_read_in, string_number, name):
        self.my_files = my_files
        self.my_path = path
        self.column_read_in = column_read_in
        print(self.my_files, self.my_path)
        self.string_number = string_number
        self.name = name
        print('xxxxxxxxxxxxx')

    def load_2_dim_array(self, file):
        nm_axis = np.loadtxt(file, skiprows=3, usecols=(0,))
        counts_per_second = np.loadtxt(file, skiprows=3, usecols=(self.column_read_in,))
        return np.transpose(np.stack((nm_axis, counts_per_second), axis=0))

    def plot_array(self, array, name, scaling_y, thickness, scaling_x):
        ax = plt.gca()
        ax.scatter(scaling_x * abs(array[::, 0]), scaling_y * array[::, 1], label=name, linewidth=thickness)
        ax.set_yscale('log')
        ax.set_xscale('log')
        plt.xlabel('eV')
        plt.ylabel('signal/s *' + name)
        plt.legend()

    def process_files(self, scaling_y, linewidth, scaling_x):
        for counter, value in enumerate(self.my_files):
            file = self.my_path + '/' + value
            print(value, 'processing...')
            spectrum_x = self.load_2_dim_array(file)
            self.plot_array(spectrum_x, self.name, scaling_y, linewidth, scaling_x)


def get_file_list(my_file, name):
    my_files = []
    counter = 0
    for file in os.listdir(my_file):
        try:
            if file.endswith(name + ".txt"):
                my_files.append(str(file))
                counter = counter + 1
                print(str(file))
            else:
                print("only other files found")
        except Exception as e:
            raise e
    return my_files


file_path = 'W_high_E'
add = 'Nphoton_sr_filter_bw'
my_files_as_list = get_file_list(file_path, add)
print(my_files_as_list)

single = my_files_as_list
print('single first element', single[-1])

Test = PlotAndStitch(file_path, single, 1, -25, add)
Test.process_files(1, 1, 1)

plt.xlim(50, 1600)
plt.savefig("W_target_" + add + ".png", bbox_inches="tight", dpi=500)
plt.show()
