import matplotlib.pyplot as plt
import numpy as np
import os


class PlotAndStitch:
    def __init__(self, path, my_files, column_read_in, string_number, name, lower_limit, upper_limit):
        self.my_files = my_files
        self.my_path = path
        self.column_read_in = column_read_in
        print(self.my_files, self.my_path)
        self.string_number = string_number
        self.name = name
        self.my_lower_limit = lower_limit
        self.upper_limit = upper_limit

    def load_2_dim_array(self, file):
        nm_axis = np.loadtxt(file, skiprows=3, usecols=(0,))
        counts_per_second = np.loadtxt(file, skiprows=3, usecols=(self.column_read_in,))
        return np.transpose(np.stack((nm_axis, counts_per_second), axis=0))

    def plot_array(self, array, name, scaling_y, linewidth, scaling_x):
        ax = plt.gca()
        ax.scatter(scaling_x * abs(array[::, 0]), scaling_y * array[::, 1], label=name, linewidth=linewidth)
        ax.set_yscale('log')
        ax.set_xscale('log')
        plt.xlabel('eV')
        plt.ylabel('Nphoton/s*sr @ 0.1% bw')
        plt.legend()

    def prepare_header(self, name2, border, array):
        # insert header line and change index
        header_names = (['eV', name2])
        parameter_info = ([name2, '_border_index_' + border])
        info = np.vstack((parameter_info, header_names))

        return np.vstack((info, array))

    def save_data(self, name2, borders, array):
        result = self.prepare_header(name2, borders, array)
        np.savetxt(name2 + 'selection' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')

    def process_files(self, scaling_y, linewidth, scaling_x, name_list):
        result = np.empty([])
        for counter, value in enumerate(self.my_files):
            file = self.my_path + '/' + value
            print(value, 'processing...')
            spectrum_x = self.load_2_dim_array(file)[self.my_lower_limit[counter]:self.upper_limit[counter]]
            name = str(value)[:self.string_number]
            # self.get_filter_name(value)
            self.plot_array(spectrum_x, name_list[counter], scaling_y, linewidth, scaling_x)
            self.save_data(name, str(self.my_lower_limit[counter]) + ':' + str(self.upper_limit[counter]) + str(
                name_list[counter]), spectrum_x)

        # plt.ylim(0,4E7)
        # plt.show()
        print(result)


def get_file_list(my_path, name):
    my_files = []
    counter = 0
    for file in os.listdir(my_path):
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


file_path = 'W_target_converted/selection'
add = 'Nphoton_sr_filter_bw_TG'
my_files_as_list = get_file_list(file_path, add)
my_lower_limit = np.array([10, 250, 5, 5, 20, 5, 10, 10])
my_upper_limit = np.array([-10, -20, -30, -30, -1, -3, -2, -1])
my_name_list = ['Zr_298nm', 'Zr_298nm', 'zr_298nm', 'Zr_298nm', 'Al_200nm', 'Al_200nm', 'Al_200nm', 'bla']

print(my_name_list[1])
print(my_files_as_list)
single = my_files_as_list

print('single first element', single[-1])

Test = PlotAndStitch(file_path, single, 1, -25, add, my_lower_limit, my_upper_limit)
Test.process_files(1, 1, 1, my_name_list)

plt.xlim(50, 1600)
# plt.ylim(0, 1.5E4)
plt.savefig("W_target_" + add + ".png", bbox_inches="tight", dpi=500)
plt.show()
