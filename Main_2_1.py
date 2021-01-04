import matplotlib.pyplot as plt
import numpy as np
import os


def load_2_dim_array(file, column_x, column_y):
    nm_axis = abs(np.loadtxt(file, skiprows=3, usecols=(column_x,)))
    counts_per_second = np.loadtxt(file, skiprows=3, usecols=(column_y,))
    return np.transpose(np.stack((nm_axis, counts_per_second), axis=0))


# labbook page 9: CCD-grating 35cm # grating RZP wall 61,5 cmm + RZP: 39 cm #
# rZP chamber = 111,5 cm # wall out to source 17,5
# distance_source = 0.35 + 0.615 + 0.390 + 1.115 + 0.175


file_path = 'W_target/20201021'
measurement_array = load_2_dim_array(file_path, 1, 2)
file_name = str(file_path)[9:24]
print(file_name)


class NPhotonPerSr:
    def __init__(self, array, name):
        self.array = array[:-55]
        self.array[::, 0] = abs(self.array[::, 0])
        self.array = self.order_ascending()
        print(self.array[-1, 0], self.array[1, 0])
        self.result = self.array[:-1]
        self.name = name

    def order_ascending(self):
        return self.array[self.array[:, 0].argsort()]

    def plot_initial(self):
        plt.figure(1)
        plt.plot(self.array[::, 0], self.array[::, 1], label='initial spectrum')
        plt.ylabel('counts/s')
        plt.xlabel('eV')
        plt.legend()

    def per_sr(self):
        self.array[::, 1] = self.array[::, 1] / (2.144 * 1E-8)
        return self.array

    def prepare_ccd_cal(self, file):
        energy = abs(np.loadtxt(file, skiprows=2, usecols=(0,)))
        count_cam = np.loadtxt(file, skiprows=2, usecols=(1,))
        array_cam = np.transpose(np.stack((energy, count_cam), axis=0))
        return array_cam

    def load_filter(self, file, name):
        nm_axis = abs(np.loadtxt(file, skiprows=3, usecols=(0,)))
        transmission_values = np.loadtxt(file, skiprows=3, usecols=(1,))
        plt.figure(1)
        plt.plot(nm_axis, transmission_values * 1E4, label=name)
        plt.legend()

        return np.transpose(np.stack((nm_axis, transmission_values), axis=0))

    def photon_numbers(self):
        calibration_cam = self.prepare_ccd_cal('Andor_cal_file_interpolated.txt')
        for counter, value in enumerate(self.array[::, 0]):
            counts_cam = calibration_cam[np.where(calibration_cam[::, 0] >= value)[0][0], 1]
            self.array[counter, 1] = self.array[counter, 1] / (counts_cam * value)
        return self.array

    def band_width_normalization(self):
        neighbor = self.array[1:, 0]
        bw_measured = -1 * self.result[::, 0] + neighbor[::]
        bw_wanted = self.result[::, 0] / 1000
        ratio_difference = bw_measured[::] / bw_wanted[::]
        self.result[::, 1] = self.result[::, 1] / ratio_difference
        return self.result

    def correct_for_filter(self, path, name):
        array_filter_interpolated = self.load_filter(path, name)
        # print('test antes:', self.result[100])
        for counter, value in enumerate(self.result[::, 0]):
            print(value)
            index = np.where(array_filter_interpolated[::, 0] >= value)[0][0]
            print(array_filter_interpolated[index], 'filter value')
            print(self.result[counter], 'array value')

            self.result[counter, 1] = self.result[counter, 1] / array_filter_interpolated[index, 1]

        # print('test danach', self.result[100])
        self.plot_it(array_filter_interpolated, 'fitler')
        self.plot_it(self.result, name)
        return self.result

    def plot_it(self, array, name):
        plt.figure(4)
        plt.plot(array[::, 0], array[::, 1], label=name)
        plt.xlabel('eV')
        plt.legend()

    def prepare_header(self, name_filter, name2):
        # insert header line and change index
        header_names = (['eV', name2])
        parameter_info = ([self.name + name2, '_used_filters:_' + name_filter])
        info = np.vstack((parameter_info, header_names))

        return np.vstack((info, self.result))

    def save_data(self, name_filter, name2):
        result = self.prepare_header(name_filter, name2)
        plt.figure(4)

        # plt.savefig(self.name + name2 + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(self.name + name2 + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


Test = NPhotonPerSr(measurement_array, file_name)
Test.plot_initial()
Test.per_sr()
Test.save_data('sr', '_sr_corrected')
Test.photon_numbers()
Test.save_data('ccd', '_Nphoton_sr')
Test.band_width_normalization()
Test.save_data('bw_corrected', '_Nphoton_sr_bw')
Test.correct_for_filter('Zr_298nm_eV_interpolated.txt', 'Zr')
Test.save_data('Zr_corrected', '_Nphoton_sr_filter_bw')
Test.correct_for_filter('TG_efficiency_in_eV_interpolated.txt', '_Nphoton_sr_filter_bw_TG')
Test.save_data('TG_corrected', '_Nphoton_sr_filter_bw_TG')

# reduced_2 = Test.correct_for_filter('TG_efficiency_in_eV.txt', 'TG')

plt.plot()
plt.show()
