#
# Calibration of Merton s (1976)
# Jump Diffusion Model
# via Fast Fourier Transform
# M76_Calibration_FFT.py
#
# (c) Dr. Yves J. Hilpisch
# Script for illustration purposes only.
#
import scipy.optimize as sop
from matplotlib.pyplot import *
from M76_Valuation_FFT import *
#
# Market Data from www.eurexchange.com
# as of 25. August 2009
#
T = array((115. / 365, 206. / 365, 297. / 365))
S0 = 2801.14 # EURO STOXX 50 Level
r = 0.025
Kl = arange(2700 , 3301 , 50)
C0 = zeros ((len(T), len(Kl)), f )
C0[0] = array (( 211.1, 179.8, 151.0, 124.8, 101.5, 81.2,
        63.9, 49.6, 37.9, 28.7, 21.4, 15.9, 11.7))
C0[1] = array (( 262.0, 231.7, 203.3, 177.0, 152.7, 130.6,
        110.6, 92.8, 77.1, 63.4, 51.6, 41.5, 33.1))
C0[2] = array (( 271.8, 243.7, 217.2, 192.4, 169.4, 148.2,
        128.8, 111.2, 95.4, 81.4, 69.0, 58.1, 48.7))

#
# Error Function
#

def M76_Error_Function_FFT(p0):
    '''Error Function for Parameter Calribration in M76 Model via
    Carr -Madan (1999) FFT Approach.
    sigma: volatility factor in diffusion term
    lamb: jump intensity
    mu: expected jump size
    delta: standard deviation of jump '''
    sigma , lamb , mu , delta = p0
    M76C0 = zeros ((len(T), len(Kl)), d )
    pen = 0.0
    if sigma < 0.0 or delta < 0.0 or lamb < 0.0:
        pen = 100.0
    for i in range(len(T)):
        for j in range(len(Kl)):
            M76C0[i, j] = M76_Value_Call_FFT(S0 , Kl[j],
                                T[i], r, sigma , lamb , mu, delta)
    RMSE = sqrt(sum(sum((C0 - M76C0) ** 2)) / len(C0)) + pen
    print p0 , RMSE
    return RMSE


#
# Calibration
#

opt1 = sop.brute(M76_Error_Function_FFT , ((0.19 , 0.21 , 0.01),
                (0.20, 0.30 , 0.01), (-0.1, -0.03, 0.01),
                (0.09, 0.12 , 0.01)), finish=None)

opt2 = sop.fmin(M76_Error_Function_FFT , opt1 ,
                maxiter=500 , maxfun=1000)

#
# Calculating Model Prices
#
M76P = zeros ((len(T), len(Kl)), d )
sigma , lamb , mu , delta = opt2
for i in range(len(T)):
    listV = []
    for j in range(len(Kl)):
        listV.append(M76_Value_Call_FFT(S0 , Kl[j],
                        T[i], r, sigma , lamb , mu, delta))
    M76P[i] = array(listV)
#
# Graphical Output
#

xlabel( 'Strike' )
ylabel( 'European Call Option Value' )
grid(True)
plot(Kl , C0[0], 'b' )
plot(Kl , M76P[0], 'bo' )
plot(Kl , C0[1], 'r' )
plot(Kl , M76P[1], 'rx' )
plot(Kl , C0[2], 'g' )
plot(Kl , M76P[2], 'g>' )
