"""
Compute sensitivity kernels for Love waves.

:copyright:
    Andreas Fichtner (andreas.fichtner@erdw.ethz.ch), November 2013
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""

def kernels_sh(r, l1, l2, _omega, _k, I3, rho, A, C, F, L, N, write_output, output_directory, tag):
	"""
	Compute and write sensitivity kernels for Love waves.

	kernels_sh(r, l1, l2, _omega, _k, I3, L, write_output, output_directory, tag)
	"""

	import numpy as np

	#- initialisations ----------------------------------------------------------------------------

	K_rho_0 = np.zeros(len(r))
	K_A_0 = np.zeros(len(r))
	K_C_0 = np.zeros(len(r))
	K_F_0 = np.zeros(len(r))
	K_L_0 = np.zeros(len(r))
	K_N_0 = np.zeros(len(r))

	K_rho = np.zeros(len(r))
	K_vph = np.zeros(len(r))
	K_vpv = np.zeros(len(r))
	K_vsh = np.zeros(len(r))
	K_vsv = np.zeros(len(r))
	K_eta = np.zeros(len(r))

	vpv = np.sqrt(A/rho)
	vph = np.sqrt(C/rho)
	vsh = np.sqrt(N/rho)
	vsv = np.sqrt(L/rho)
	eta = F / (A-2*L)

	#- compute fundamental kernels ----------------------------------------------------------------


	K_rho_0 = -(_omega**3 * l1**2) / (2 * _k**3 * I3)
	K_A_0 = np.zeros(len(l1))
	K_C_0 = np.zeros(len(l1))
	K_F_0 = np.zeros(len(l1))
	K_L_0 = (_omega * l1**2) / (2 * _k**3 * I3 * L**2)
	K_N_0 = (_omega * l1**2) / (2 * _k * I3)

	#- compute relative kernels in velocity parametrisation ---------------------------------------

	K_vph = 2*A*K_A_0 + 2*A*eta*K_F_0
	K_vpv = 2*C*K_C_0
	K_vsh = 2*N*K_N_0
	K_vsv = 2*L*K_L_0 - 4*L*eta*K_F_0
	K_rho = rho*K_rho_0 + N*K_N_0 + L*K_L_0
	K_eta = F*K_F_0

	#- convert to relative kernels ----------------------------------------------------------------

	K_rho_0 = rho*K_rho_0
	K_L_0 = L*K_L_0
	K_N_0 = N*K_N_0

	#- write results to file ----------------------------------------------------------------------

	if write_output:

		identifier = "T="+str(2*np.pi/_omega)+".c="+str(_omega / _k)
		fid = open(output_directory+"kernels_sh."+tag+"."+identifier,"w")
		fid.write("number of vertical sampling points\n")
		fid.write(str(len(r))+"\n")
		fid.write("radius K_rho_0 K_A_0 K_C_0 K_F_0 K_L_0 K_N_0 K_rho K_vph K_vpv K_vsh K_vsv K_eta\n")
		for idx in np.arange(len(r)):
			fid.write(str(r[idx])+" "+str(K_rho_0[idx])+" "+str(K_A_0[idx])+" "+str(K_C_0[idx])+" "+str(K_F_0[idx])+" "+str(K_L_0[idx])+" "+str(K_N_0[idx])+" "+str(K_rho[idx])+" "+str(K_vph[idx])+" "+str(K_vpv[idx])+" "+str(K_vsh[idx])+" "+str(K_vsv[idx])+" "+str(K_eta[idx])+"\n")
		fid.close()