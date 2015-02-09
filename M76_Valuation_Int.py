#
# Valuation of European Call Options
# in Merton s (1976) Jump Diffusion Model
# via Numerical Integration
# M76_Valuation_Int.py
#
# (c) Dr. Yves J. Hilpisch
# Script for illustration purposes only.
#
from numpy import *
from scipy.integrate import *
#
# Model Parameters
#
S0 = 100.0 # Initial Index Level
K = 100.0 # Strike Level
T = 1.0 # Call Option Maturity
r = 0.05 # Constant Short Rate
sigma = 0.4 # Constant Volatility of Diffusion
lamb = 1.0 # Jump Frequency p.a.
mu = -0.2 # Expected Jump Size
delta = 0.1 # Jump Size Volatility
#
# Valuation by Integration
#

def M76_Value_Call_Int(S0, K, T, r, sigma , lamb , mu, delta):
    ''' Valuation of European Call Option in M76 Model via Lewis (2001)
    Fourier -based Approach.
    S0: initial stock/index level
    K: strike price
    T: time -to -maturity (for t=0)
    r: constant risk -free short rate
    sigma: volatility factor in diffusion term
    lamb: jump intensity
    mu: expected jump size
    delta: standard deviation of jump '''
    Int = quad(lambda u: M76_Int_Func(u, S0, K, T, r,
                    sigma , lamb , mu , delta), 0, 50 , limit=250)[0]
    return (S0 - exp(-r * T) * sqrt(S0 * K) / pi * Int)

def M76_Int_Func(u, S0 , K, T, r, sigma , lamb , mu , delta ):
    ''' Valuation of European Call Option in M76 Model via Lewis (2001)
    Fourier -based Approach: Integration Function.
    Parameter definitions see function M76_Value_Call_Int. '''
    JDCF = M76_Char_Func(u - 0.5 * 1j , T, r, sigma , lamb , mu , delta)
    return 1 / (u ** 2 + 0.25) * (exp(1j * u * log(S0 / K)) * JDCF).real

def M76_Char_Func(u, T, r, sigma , lamb , mu , delta ):
    ''' Valuation of European Call Option in M76 Model via Lewis (2001)
    Fourier -based Approach: Characteristic Function.
    Parameter definitions see function M76_Value_Call_Int. '''
    omega = r - 0.5 * sigma ** 2 - lamb * (exp(mu + 0.5 * delta ** 2) - 1)
    return exp((1j * u * omega - 0.5 * u ** 2 * sigma ** 2 +
            lamb * (exp(1j * u * mu - u ** 2 * delta ** 2 * 0.5) - 1)) * T)
print "Value of Call Option %8.3f" \
    % M76_Value_Call_Int(S0, K, T, r, sigma, lamb, mu, delta)


