#
# Calibration of Merton s (1976)
# Jump Diffusion Model
# to Short Maturity Data
# M76_Calibration_Short.py
#
# (c) Dr. Yves J. Hilpisch
# Script for illustration purposes only.
#
from matplotlib.pyplot import *
from M76_Valuation_FFT import *
from scipy.optimize import brute , fmin
#
# Market Data from www.eurexchange.com
# as of 25. August 2009
#
S0 = 2801.14
T = 115. / 365
r = 0.025
Kl = arange(2700 , 2901 , 50)
C0 = array ((211.1, 179.8, 151.0, 124.8, 101.5))
#
# Error Function
#

def M76_Error_Function_FFT(p0):
    '''Error Function for Parameter Calribration in M76 Model via
    Carr-Madan (1999) FFT Approach.
    sigma: volatility factor in diffusion term
    lamb: jump intensity
    mu: expected jump size
    delta: standard deviation of jump '''
    sigma , lamb , mu , delta = p0
    M76C0 = zeros(len(Kl), 'd' )
    pen = 0.0
    if sigma < 0.0 or delta < 0.0 or lamb < 0.0 or lamb > 0.8:
        pen = 100.0
    for j in range(len(Kl)):
        M76C0[j] = M76_Value_Call_FFT(S0 , Kl[j], T, r,
                        sigma , lamb , mu , delta)
    RMSE = sqrt(sum(sum((C0 - M76C0) ** 2)) / len(C0)) + pen
    print p0 , RMSE
    return RMSE

#
# Calibration
#
opt1 = brute(M76_Error_Function_FFT , ((0.14 , 0.24 , 0.02),
                (0.0, 0.8, 0.1), (-0.4, 0.0, 0.05),
                (0.00, 0.12 , 0.02)), finish=None)
opt2 = fmin(M76_Error_Function_FFT , opt1 , xtol=0.00001 ,
            ftol=0.00001 , maxiter=750 , maxfun=1500)
### Results (rounded)
# sigma = 0.1636
# lamb = 0.7473
# mu =-0.1918
# delta = 0.0000

#
# Graphical Output
#
M76P = zeros(len(Kl), d )
sigma , lamb , mu , delta = opt2
listV = []
for K in Kl:
    listV.append(M76_Value_Call_FFT(S0 , K, T, r,
                            sigma , lamb , mu , delta ))
M76P = array(listV)
xlabel( 'Strike' )
ylabel( 'European Call Option Value' )
grid(True)
plot(Kl , C0 , 'b' )
plot(Kl , M76P , 'ro' )
