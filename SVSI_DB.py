#
# Creating a Database for Simulation Results for
# American put options in H93 and CIR85 model
# SVSI_DB.py
#
# (c) Dr. Yves J. Hilpisch
# Script for illustration purposes only.
#
from tables import *
from numpy import *
from datetime import datetime
#
# Record to Store Simulation Results
#


class SimResult(IsDescription):

		#	Description of Table to Store Simulation Results.   #
			
    sim_name = StringCol(32 , pos=2)
	seed = Int32Col(pos=3)
	x_disc = StringCol(26 , pos=4)
	runs = Int32Col(pos=5)
	time_steps = Int32Col(pos=6)
	paths = Int32Col(pos=7)
	con_var = StringCol(8, pos=8)
	mo_match = StringCol(8, pos=9)
	anti_paths = StringCol(8, pos=10)
	base_funcs = Int32Col(pos=11)
	opt_prices = Int32Col(pos=12)
	abs_tol = Float32Col(pos=13)
	rel_tol = Float32Col(pos=14)
	errors = Int32Col(pos=15)
	error_ratio = Float32Col(pos=16)
	av_val_err = Float32Col(pos=17)
	ab_val_err = Float32Col(pos=18)
	mse_val_err = Float32Col(pos=19)
	av_rel_err = Float32Col(pos=20)
	ab_rel_err = Float32Col(pos=21)
	mse_rel_err = Float32Col(pos=22)
	time_sec = Float32Col(pos=23)
	time_min = Float32Col(pos=24)
	time_opt = Float32Col(pos=25)
	start_date = StringCol(26 , pos=26)
	end_date = StringCol(26 , pos=27)
	
#
# Record to Store Single Valuation Results
#

class ValResult(IsDescription):	

		# Description of Table to store Single Valuation Results  #

	sim_name = StringCol(32 , pos=2)
	panel = Int32Col(pos=3)
	opt_T = Float32Col(pos=4)
	opt_K = Float32Col(pos=5)
	euro_ana = Float32Col(pos=6)
	euro_mcs = Float32Col(pos=7)
	am_right_val = Float32Col(pos=8)
	am_lsm_pure = Float32Col(pos=9)
	am_lsm_cova = Float32Col(pos=10)
	am_lsm_se = Float32Col(pos=11)
	correct = StringCol(8, pos=12)
	val_err_abs = Float32Col(pos=13)
	val_err_rel = Float32Col(pos=14)
	x_disc = StringCol(26 , pos=15)
	time_steps = Int32Col(pos=16)
	paths = Int32Col(pos=17)
	con_var = StringCol(8, pos=18)
	mo_match = StringCol(8, pos=19)
	anti_paths = StringCol(8, pos=20)
	base_funcs = Int32Col(pos=21)
	val_date = StringCol(26 , pos=22)
	
# Generate new file for simulation results  #

filename = "./ Results/Book_DAWP_SVSI_LSM.h5"

def CreateFile(filename):
		 # Creates an HDF5 File as Database for Results. #
		 
	h5file = openFile(filename , mode= 'w' , title= 'SVSI_LSM' )
	group = h5file.createGroup(h5file.root , 'results' , 'Results' )
	h5file.createTable(group , 'Sim_Results' , SimResult, 'Simulation Results' )
	h5file.createTable(group , 'Val_Results' , ValResult, 'Valuation Results' )
	h5file.close ()

#
# Fill the table with simulation results
#

def ResWrite(filename , name , SEED , xDisc , R, M, I, coVar , moMatch ,
			 antiPaths , D, l, atol , rtol , errors , absError , relError ,
			 t1 , t2 , d1 , d2):
	Writes Simulation Results to Database Table.
	h5file = openFile(filename , mode= a )
	table = h5file.root.results.Sim_Results
	simres = table.row
	simres[ sim_name ] = name
	simres[ seed ] = SEED
	simres[ runs ] = R
	simres[ time_steps ] = M
	simres[ x_disc ] = xDisc
	simres[ paths ] = I
	simres[ con_var ] = coVar
	simres[ mo_match ] = moMatch
	simres[ anti_paths ] = antiPaths
	simres[ base_funcs ] = D
	simres[ opt_prices ] = l
	simres[ abs_tol ] = atol
	simres[ rel_tol ] = rtol
	simres[ errors ] = errors
	simres[ error_ratio ] = errors / l
	simres[ av_val_err ] = sum(array(absError)) / l
	simres[ ab_val_err ] = sum(abs(array(absError ))) / l
	simres[ mse_val_err ] = sum(array(absError) ** 2) / l
	simres[ av_rel_err ] = sum(array(relError)) / l
	simres[ ab_rel_err ] = sum(abs(array(relError ))) / l
	simres[ mse_rel_err ] = sum(array(relError) ** 2) / l
	simres[ time_sec ] = t2 - t1
	simres[ time_min ] = (t2 - t1) / 60
	simres[ time_opt ] = (t2 - t1) / l
	simres[ start_date ] = d2
	simres[ end_date ] = d1
	simres.append ()
	table.flush ()
	h5file.close ()

#
# Fill the table with single valuation results
#

def ValWrite(h5file , name , panel , T, K, P0, P0_MCS , tValue , A0LS , A0CV , SE,
			 CORR , xDisc , M, I, coVar , moMatch , antiPaths , D, date ):
	#  Writes Single Valuation Results to Database Table.  #
	table = h5file.root.results.Val_Results
	valres = table.row
	valres[ sim_name ] = name
	valres[ panel ] = panel + 1
	valres[ opt_T ] = T
	valres[ opt_K ] = K
	valres[ euro_ana ] = P0
	valres[ euro_mcs ] = P0_MCS
	valres[ am_right_val ] = tValue
	valres[ am_lsm_pure ] = A0LS
	valres[ am_lsm_cova ] = A0CV
	valres[ am_lsm_se ] = SE
	valres[ correct ] = CORR
	valres[ val_err_abs ] = A0CV - tValue
	valres[ val_err_rel ] = (A0CV - tValue) / tValue
	valres[ x_disc ] = xDisc
	valres[ time_steps ] = M
	valres[ paths ] = I
	valres[ con_var ] = coVar
	valres[ mo_match ] = moMatch
	valres[ anti_paths ] = antiPaths
	valres[ base_funcs ] = D
	valres[ val_date ] = date
	valres.append ()
	table.flush ()
	
#
# Read and Print Simulation Results
#

def PrintResults(filename=filename , idl=0, idh=25):
   '''   Prints Simulation Results (Full ).   
	filename: name of HDF5 database file
	idl: starting index 
	idh: end index '''
	h5file = openFile(filename , mode= a )
	simres = h5file.root.results.Sim_Results
	br = "----------------------------------------------------"
	
for i in range(idl , min(len(simres), idh + 1)):
	print br
	print "Start Calculations %32s" \
		% simres[i][ start_date ] \
		+ "\n" + br
	print "Name of Simulation %32s" % simres[i][ sim_name ]
	print "Seed Value for RNG %32d" % simres[i][ seed ]
	print "Discretization %32s" % simres[i][ x_disc ]
	print "Number of Runs %32d" % simres[i][ runs ]
	print "Time Steps %32d" % simres[i][ time_steps ]
	print "Paths %32d" % simres[i][ paths ]
	print "Control Variates %32s" % simres[i][ con_var ]
	print "Moment Matching %32s" % simres[i][ mo_match ]
	print "Antithetic Paths %32s" % simres[i][ anti_paths ]
	print "Basis Functions %32d" % simres[i][ base_funcs ] + "\n"
	print "Option Prices %32d" % simres[i][ opt_prices ]
	print "Absolute Tolerance %32.4f" % simres[i][ abs_tol ]
	print "Relative Tolerance %32.4f" % simres[i][ rel_tol ]
	print "Errors %32d" % simres[i][ errors ]
	print "Error Ratio %32.4f" % simres[i][ error_ratio ] + "\n"
	print "Aver Val Error %32.4f" % simres[i][ av_val_err ]
	print "Aver Abs Val Error %32.4f" % simres[i][ ab_val_err ]
	print "MSE Val Error %32.4f" % simres[i][ mse_val_err ] + "\n"
	print "Aver Rel Error %32.4f" % simres[i][ av_rel_err ]
	print "Aver Abs Rel Error %32.4f" % simres[i][ ab_rel_err ]
	print "MSE Rel Error %32.4f" % simres[i][ mse_rel_err ] + "\n"
	print "Time in Seconds %32.4f" % simres[i][ time_sec ]
	print "Time in Minutes %32.4f" % simres[i][ time_min ]
	print "Time per Option %32.4f" % simres[i][ time_opt ] + "\n" + br
	print "End Calculations %32s" \
		% simres[i][ end_date ] \
		+ "\n" + br + "\n"
	print "Total number of rows in table %d" % len(simres)
	h5file.close ()

#
# Read and Print Simulations Results (Short Form and Latex Output)
#

def PrintRes(filename=filename , idl=0, idh=50):
	'''Prints Simulation Results (Partial ).
	filename: name of HDF5 database file
	idl: starting index
	idh: end index'''
	h5file = openFile(filename , mode="r")
	simres = h5file.root.results.Sim_Results
	br = "-----------------------------------------------------------"
	for i in range(idl , min(len(simres), idh + 1)):
		print br
		print "Name of Simulation %39s" % simres[i][ sim_name ]
		print ("Paths %18d" % simres[i][ paths ]
			+ " Errors %9d" % simres[i][ errors ])
		print ("Aver Val Error %9.4f" % simres[i][ av_val_err ]
			+ " Time per Opt. %9.4f" % simres[i][ time_opt ]
			+ "\n" + br)
		print "Total number of rows in table %d" % len(simres)
		h5file.close ()

		
def PrintTex(filename=filename , idl=0, idh=100):
	'''Generates Latex Code for Simulation Results.
	filename: name of HDF5 database file
	idl: starting index
	idh: end index'''
	h5file = openFile(filename , mode="r")
	simres = h5file.root.results.Sim_Results
	for i in range(idl , min(len(simres), idh + 1)):
		if simres[i][ paths ] != 15000:
			out1 = "%2d & %3d & %3d & %s & %s &"
			out2 = " %s & %s & %3d & %3d & %4.3f & %5.3f \\tn"
			out = out1 + out2
			print out \
				% (simres[i][ runs ], simres[i][ time_steps ],
				simres[i][ paths ] / 1000, simres[i][ x_disc ][0],
				simres[i][ con_var ], simres[i][ mo_match ],
				simres[i][ anti_paths ], simres[i][ opt_prices ],
				simres[i][ errors ], simres[i][ av_val_err ],
				simres[i][ time_opt ])
	print "Total number of rows in table %d" % len(simres)
	h5file.close ()
	
#
# Read and Print Valuation Results
#

def PrintValResults(filename=filename , idl=0, idh=20):
	'''Prints Single Valuation Results.
	filename: name of HDF5 database file
	idl: starting index
	idh: end index'''
	h5file = openFile(filename , mode= r )
	valres = h5file.root.results.Val_Results
	br = "--------------------------------------------------------------"
	for i in range(idl , min(len(valres), idh + 1)):
		print br
		print "Valuation Date %32s" \
			% valres[i][ val_date ] + "\n" + br
		print "Name of Simulation %32s" % valres[i][ sim_name ]
		print "Panel %32d" % valres[i][ panel ]
		print " Option Maturity %32.4f" % valres[i][ opt_T ]
		print " Results for Strike %32d" % valres[i][ opt_K ]
		print " European Put Value MCS %32.4f" % valres[i][ euro_mcs ]
		print " European Put Value Closed %32.4f" % valres[i][ euro_ana ]
		print " American Put Value LSM %32.4f" % valres[i][ am_lsm_pure ]
		print " American Put Value CV %32.4f" % valres[i][ am_lsm_cova ]
		print " Standard Error LSM CV %32.4f" % valres[i][ am_lsm_se ]
		print " American Put Value Paper %32.4f" \
			% valres[i][ am_right_val ]
		print " Valuation Correct %32s" % valres[i][ correct ]
		print " Valuation Error (abs) %32.4f" % valres[i][ val_err_abs ]
		print " Valuation Error (rel) %32.4f" \
			% valres[i][ val_err_rel ] + "\n" + br
		print "Discretization %32s" % valres[i][ x_disc ]
		print "Time Steps %32d" % valres[i][ time_steps ]
		print "Paths %32d" % valres[i][ paths ]
		print "Control Variates %32s" % valres[i][ con_var ]
		print "Moment Matching %32s" % valres[i][ mo_match ]
		print "Antithetic Paths %32s" % valres[i][ anti_paths ]
		print "Basis Functions %32d" \
			% valres[i][ base_funcs ] + "\n" + br + "\n"
		print "Total number of rows in table %d" % len(valres)
		h5file.close ()
		
		
		







































	
	
	
	
	
	
	