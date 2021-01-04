import numpy as np
import os
import matplotlib.pyplot as plt


class SearchForEnergies:

    def __init__(self, my_path, energy):
        self.path = my_path
        self.energy = energy
        self.index = int
        self.result = np.zeros([1, 2])
        print(self.result)

    def load_2_dim_array(self, file):
        my_file = self.path + '/' + file
        ev_axis = np.loadtxt(my_file, skiprows=3, usecols=(0,))
        counts = np.loadtxt(my_file, skiprows=3, usecols=(1,))
        return np.transpose(np.stack((ev_axis, counts), axis=0))

    def get_file_list(self, attribute):
        my_files = []
        counter = 0
        print(attribute)
        for file in os.listdir(self.path):
            try:
                if file.endswith(attribute + ".txt"):
                    my_files.append(str(file))
                    counter = counter + 1
                    print(str(file))

            except Exception as e:
                raise e

        self.batch(my_files)
        return my_files

    def search_energy(self, array, energy):
        max = np.amax(array[::, 0])
        min = np.amin(array[::, 0])

        if max > energy > min:
            print(max)
            x = np.where(array[::, 0] >= energy)[0][0]
            print(x, array[x])
        else:
            x = None

        return x

    def test_energy_range(self, array, energy):
        if np.amax(array[::, 0]) < energy:
            pass

        else:
            x = self.search_energy(array, energy)

            return x

    def process_energy_list(self, array):
        for counter, value in enumerate(self.energy):
            # print(value, 'energy selected')
            self.index = self.test_energy_range(array, value)
            if self.index is not None:
                # print(array[self.index].reshape(1,2))
                # print('previous',self.result,'new', array[self.index], self.index)
                # print(self.result.shape, array[self.index].shape)
                self.result = np.concatenate((self.result, array[self.index].reshape(1, 2)), axis=0)
        # print(self.result)
        return self.result

    def batch(self, files):
        for counter, value in enumerate(files):
            print(value, 'file')
            array = self.load_2_dim_array(value)
            self.result = self.process_energy_list(array)
        return self.result

    def calc_error(self):
        ccd_rel = 0.05
        tg_rel = 0.2
        filter_rel = 0.1
        err_y = np.zeros([len(self.result)])

        for counter, value in enumerate(self.result[::, 1]):
            error_rel = (ccd_rel ** 2 + tg_rel ** 2 + filter_rel ** 2) ** 0.5
            err_y[counter] = error_rel * value
        self.plot_with_error(err_y)
        print(self.result.shape, err_y.shape)
        self.result = np.hstack((self.result, err_y.reshape(48, 1)))
        return self.result

    def return_it(self):
        return self.result

    def plot_with_error(self, error_y):
        plt.figure(2)
        plt.errorbar(self.result[::, 0], self.result[::, 1], yerr=error_y, fmt='x', label='W')
        plt.xscale("log", nonposx='clip')
        plt.yscale("log", nonposy='clip')
        plt.ylabel('Nphoton/s*sr @ 0.1% bw')
        plt.xlabel('eV')
        plt.xlim(50, 1600)
        plt.legend()

    def prepare_header(self, name1, name2):
        # insert header line and change index
        header_names = (['eV', name2, '...'])
        parameter_info = ([name1 + name2, '_Nphoton/s*sr @ 0.1%bw:_', '....'])
        # empty = (['error absolute'])
        info = np.vstack((parameter_info, header_names))
        print(info)
        print(self.result)

        return np.vstack((info, self.result))

    def save_data(self, name1, name2):
        result = self.prepare_header(name1, name2)

        plt.figure(2)
        plt.savefig(name1 + name2 + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(name1 + name2 + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


energy_list = (
    60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 170, 200, 250, 270, 300, 350, 400, 450, 500,
    600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600)
path = 'W_high_E/selection'
Test_500eV = SearchForEnergies(path, energy_list)
# Test_500eV.get_file_list('_sr_corrected')
# Test_500eV.get_file_list('_Nphoton_sr')
# Test_500eV.get_file_list('Nphoton_sr_filter')
# Test_500eV.get_file_list('Nphoton_sr_filter_TG')
Test_500eV.get_file_list('_Nphoton_sr_filter_bw_TG')
Test_500eV.calc_error()
Test_500eV.save_data('W_in_units_high_E', 'selected measurements')

plt.show()
