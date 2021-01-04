# Convert_to_Nphoton_per_s_per_sr-0.001_bandwidth


A convenient unit in xray spectroscopy is: 
- Number of Photons [Nphoton]
- per second [1/s]
- per steradian [1/sr]
- @ 0.1 % bandwidth (spectrally) 


In order to approximate recorded and evaluated spectra, we need to correct them for the efficiencies and transmission of all optical elements used in the setup. Such as: 
- Transmission filters (e.g. Aluminium 200nm) see: https://henke.lbl.gov/optical_constants/
- efficiency of CCD (often given in Quantum Efficiency, e.g. counts/eV which is not constant for different energies)
- diffractive optical element (grating, zone-plate...) (usually a function of energy) see: https://henke.lbl.gov/optical_constants/

Done the detection angle is calculated into steradian, see: https://en.wikipedia.org/wiki/Steradian. It can be calculated with the distances and aperture at the grating.
And last but not least, the recorded bandwidth (of energy) has to be determined. Usually is not constant over energy, determined in this algorithm via the spectral 
distance to the next data point (next neighbor approach) and compared quantitavely to the wanted 0.1% bandwidth. 


