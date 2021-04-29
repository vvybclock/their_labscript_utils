'''
Calibrations.py for Ybclock lab.
'''

#####################################################################
#                                                                   #
# ybclock_calibrations.py                                           #
#                                                                   #
# Copyright 2021, Enrique Mendez & Simone Colombo (MIT)             #
#                                                                   #
#####################################################################

from .UnitConversionBase import *
from scipy.interpolate import interp1d
#import scipy.interp1d as interp1d


class GreenFrequencyVCOCalibration(UnitConversion):
	''' Relates the frequency shift caused on the green cavity probe beam that interrogates the vacuum Rabi splitting.
	'''
	# This is for the calibration of the VCO 1, the one normally used. In case of bicholored pulses, we will need a dedicated class for the VCO 2.


	# This must be defined outside of init, and must match the default hardware unit specified within the BLACS tab
	base_unit = 'V'
	
	# You can pass a dictionary at class instantiation with some parameters to use in your unit converstion.
	# You can also place a list of "order of magnitude" prefixes (eg, k, m, M, u, p) you also want available
	# and the UnitConversion class will automatically generate the conversion function based on the functions 
	# you specify for the "derived units". This list should be stored in the 'magnitudes' key of the parameters
	# dictionary
	
	def __init__(self, calibration_parameters = None):
		#absorb dictionary
		self.parameters = calibration_parameters
		if calibration_parameters == None:
			self.parameters = {}

		self.derived_units = ['MHz']

		# Set here the default calibration
		self.parameters.setdefault('raw_voltage', (-6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5,-1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3))
		self.parameters.setdefault('raw_frequency', (120.49,123.972,127.514,131.143,134.91,138.728,142.66,146.605,150.59,154.847,158.65,162.7,166.696,170.63,174.571,178.499,182.47,186.397,190.332))

		#define the zero frequency to be 160 MHz. Also flip the sign of the 
		self.raw_frequencies = tuple(160 - i for i in self.parameters['raw_frequency']) 

		#calculate polynomial curve
		self.interpolation_VtoHz = interp1d(self.parameters['raw_voltage'], self.raw_frequencies, kind = 'cubic',fill_value="extrapolate")
		self.interpolation_HztoV = interp1d(self.raw_frequencies, self.parameters['raw_voltage'], kind = 'cubic',fill_value="extrapolate")

		UnitConversion.__init__(self, self.parameters)
		

	def MHz_to_base(self,Mhertz):
		# uses interpolation to get converion
		volts = self.interpolation_HztoV(Mhertz)
		return volts

	def MHz_from_base(self,volts):
		# uses interpolation to get converion
		MHz = self.interpolation_VtoHz(volts)
		return MHz


