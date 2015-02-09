#
# Valuation of European Call Options
# in Merton s (1976) Jump Diffusion Model
# via Fast Fourier Transform (FFT)
# M76_Valuation_FFT.py
#
from numpy import *
from numpy.fft import *
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
# M76 Characteristic Function
#


def M76_Char_Func_SA(u, x0 , T, r, sigma , lamb , mu , delta ):
    ''' Valuation of European Call Option in M76 Model via Carr -Madan (1999)
    Fourier -based Approach (FFT): Characteristic Function.
    Parameter definitions see function M76_Value_Call_FFT. '''
    omega = x0 / T + r - 0.5 * sigma ** 2 \
    - lamb * (exp(mu + 0.5 * delta ** 2) - 1)
    return exp(1j * u * omega * T - 0.5 * u ** 2 * sigma ** 2 * T +
        lamb * T * (exp(1j * u * mu - u ** 2 * delta ** 2 * 0.5) - 1))


#
# Valuation by FFT
#

def M76_Value_Call_FFT(S0, K, T, r, sigma , lamb , mu, delta):
    ''' Valuation of European Call Option in M76 Model via Carr -Madan (1999)
    Fourier -based Approach (FFT).
    S0: initial stock/index level
    K: strike price
    T: time -to -maturity (for t=0)
    r: constant risk -free short rate
    sigma: volatility factor in diffusion term
    lamb: jump intensity
    mu: expected jump size
    delta: standard deviation of jump'''
    k = log(K / S0)
    x0 = log(S0 / S0)
    g = 2 # factor to increase accuracy
    N = g * 4096
    eps = (g * 150.) ** -1
    eta = 2 * pi / (N * eps)
    b = 0.5 * N * eps - k
    u = arange(1, N + 1, 1)
    vo = eta * (u - 1)
    # Modificatons to Ensure Integrability
    if S0 >= 0.95 * K: # ITM case
        alpha = 1.5
        v = vo - (alpha + 1) * 1j
        modcharFunc = exp(-r * T) * M76_Char_Func_SA(v, x0 , T, r, sigma ,
                                    lamb , mu , delta) / (alpha ** 2 + alpha
                                      - vo ** 2 + 1j * (2 * alpha + 1) * vo)

    else: # OTM case
        alpha = 1.1
        v = (vo - 1j * alpha) - 1j
        modcharFunc1 = exp(-r * T) * (1 / (1 + 1j * (vo - 1j * alpha ))
                                    - exp(r * T) / (1j * (vo - 1j * alpha))
                                    - M76_Char_Func_SA(v, x0, T, r, sigma,
                                        lamb , mu , delta) /
                                      ((vo - 1j * alpha) ** 2
                                       - 1j * (vo - 1j * alpha)))
        v = (vo + 1j * alpha) - 1j
        modcharFunc2 = exp(-r * T) * (1 / (1 + 1j * (vo + 1j * alpha ))
                                    - exp(r * T) / (1j * (vo + 1j * alpha))
                                    - M76_Char_Func_SA(v, x0, T, r, sigma,
                                        lamb , mu , delta) /
                                      ((vo + 1j * alpha) ** 2
                                    - 1j * (vo + 1j * alpha)))
    # Numerical FFT Routine
    delt = zeros(N, 'd' )
    delt[0] = 1
    j = arange(1, N + 1, 1)
    SimpsonW = (3 + (-1) ** j - delt) / 3
    if S0 >= 0.95 * K:
        FFTFunc = exp(1j * b * vo) * modcharFunc * eta * SimpsonW
        payoff = (fft(FFTFunc )). real
        CallValueM = exp(-alpha * k) / pi * payoff
    else:
        FFTFunc = (exp(1j * b * vo)
                    * (modcharFunc1 - modcharFunc2)
                    * 0.5 * eta * SimpsonW)
        payoff = (fft(FFTFunc )). real
        CallValueM = payoff / (sinh(alpha * k) * pi)
    pos = int((k + b) / eps)
    CallValue = CallValueM[pos]
    return CallValue * S0

print "Value of Call Option %8.3f" \
        % M76_Value_Call_FFT(S0, K, T, r, sigma, lamb, mu, delta)
        
        
