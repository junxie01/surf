"""
Computation dispersion curves and stress-displacement functions for SH propagation.

:copyright:
    Andreas Fichtner (andreas.fichtner@erdw.ethz.ch), August 2013
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""

import numpy as np
import matplotlib.pyplot as plt
import TOOLS.read_xml as rxml
import TOOLS.integrate_sh as ish

def dispersion_sh(xml_input):
	"""
	Compute dispersion curves and displacement functions for SH propagation.
	periods, phase_velocities = dispersion_sh(xml_input)
	Dispersion curves and displacement functions are written to files.
	"""

	#- read input ---------------------------------------------------------------------------------

	inp = rxml.read_xml(xml_input)
	inp = inp[1]

	verbose = int(inp["verbose"])
	plot_dispersion = int(inp["plot_dispersion"])
	plot_amplitudes = int(inp["plot_amplitudes"])

	model = inp["model"]

	write_output = inp["output"]["write_output"]
	output_directory = inp["output"]["directory"]
	tag = inp["output"]["tag"]

	r_min = float(inp["integration"]["starting_radius"])
	dr = float(inp["integration"]["radius_sampling"])

	T_min = float(inp["T_c_sampling"]["T_min"])
	T_max = float(inp["T_c_sampling"]["T_max"])
	dT = float(inp["T_c_sampling"]["dT"])

	c_min = float(inp["T_c_sampling"]["c_min"])
	c_max = float(inp["T_c_sampling"]["c_max"])
	dc = float(inp["T_c_sampling"]["dc"])

	#- initialisations ----------------------------------------------------------------------------

	T = np.arange(T_min,T_max + dT,dT,dtype=float)
	c = np.arange(c_min,c_max + dc,dc,dtype=float)
	omega = 2 * np.pi / T

	periods = []
	phase_velocities = []

	#- root-finding algorithm ---------------------------------------------------------------------

	#- loop over angular frequencies
	for _omega in omega:
		k = _omega / c

		#- loop over trial wavenumbers
		l_left = 0.0
		for n in np.arange(len(k)):

			#- compute vertical wave functions
			l1, l2, r = ish.integrate_sh(r_min, dr, _omega, k[n], model)
			l_right = l2[len(l2)-1]

			#- check if there is a zero -----------------------------------------------------------
			if l_left * l_right < 0.0:

				#- start bisection algorithm
				ll_left = l_left
				ll_right = l_right
				k_left = k[n-1]
				k_right = k[n]

				for i in np.arange(5):
					#k_new = (k_left + k_right) / 2.0
					k_new = (k_left * np.abs(ll_right) + k_right * np.abs(ll_left)) / (np.abs(ll_left) + np.abs(ll_right))
					l1, l2, r = ish.integrate_sh(r_min, dr, _omega, k_new, model)
					ll = l2[len(l2)-1]
					if ll * ll_left < 0.0:
						k_right = k_new
						ll_right = ll
					elif ll * ll_right < 0.0:
						k_left = k_new
						ll_left = ll
					else:
						continue

				#- compute final vertical wave functions
				l1, l2, r = ish.integrate_sh(r_min, dr, _omega, k_new, model)

				periods.append(2*np.pi/_omega)
				phase_velocities.append(_omega / k_new)

				#- plot and print to screen
				if verbose:
					print "T="+str(2*np.pi/_omega)+" s, c="+str(_omega / k_new)+" m/s"
				if plot_amplitudes:
					plt.plot(r, l1)
					plt.xlabel("radius [m]")
					plt.ylabel("stress-normalised displacement amplitude")
					plt.title("T="+str(2*np.pi/_omega)+" s, c="+str(_omega / k_new)+" m/s")
					plt.show()

				#- write output
				if write_output:
					identifier = "T="+str(2*np.pi/_omega)+".c="+str(_omega / k_new)
					fid = open(output_directory+"displacement_sh."+tag+"."+identifier,"w")
					fid.write("number of vertical sampling points\n")
					fid.write(str(len(r))+"\n")
					fid.write("radius displacement\n")
					for idx in np.arange(len(r)):
						fid.write(str(r[idx])+" "+str(l1[idx])+"\n")
					fid.close()

			l_left =l_right

	#- output -------------------------------------------------------------------------------------

	if write_output:

		#- write dispersion curve
		fid = open(output_directory+"dispersion_sh."+tag,"w")
		for k in np.arange(len(periods)):
			fid.write(str(periods[k])+" "+str(phase_velocities[k])+"\n")
		fid.close()

	#- plot ---------------------------------------------------------------------------------------

	if plot_dispersion:
		plt.plot(periods,phase_velocities,'ko')
		plt.plot(periods,phase_velocities,'rx')
		plt.margins(0.2)
		plt.xlabel("period [s]")
		plt.ylabel("phase velocity [m/s]")
		plt.title("SH dispersion")
		plt.show()

	#- return -------------------------------------------------------------------------------------

	return periods, phase_velocities