#
# Valuation of European Call Options
# in Merton s (1976) Jump Diffusion Model
# via Monte Carlo Simulation
# M76_Valuation_MCS.py
#
# (c) Dr. Yves J. Hilpisch
# Script for illustration purposes only.
#
from pylab import *
from M76_Valuation_FFT import M76_Value_Call_FFT
from M76_Valuation_Int import M76_Value_Call_Int
#
# Model Parameters (from Calibration)
#
S0 = 82610. # Initial Index Level
T = 6. / 365 # Call Option Maturity
r = 0.0 # Constant Short Rate
sigma = 0.494 # Constant Volatility of Diffusion
lamb = 0.541 # Jump Frequency p.a.
mu = -9.058 # Expected Jump Size
delta = 0. # Jump Size Volatility

#
# Valuation by Simulation
#

seed = 100000 # seed Value RNG
M = 50 # time steps
I = 200000 # paths
disc = 2 # 1 = simple Euler; else = log Euler

def M76_Simulation(S0, T, r, sigma , lamb , mu , delta , M, I):
    '''Generate Monte Carlo Paths for M76 Model.
    S0: initial stock/index level
    T: time -to -maturity (for t=0)
    r: constant risk -free short rate
    sigma: volatility factor in diffusion term
    lamb: jump intensity
    mu: expected jump size
    delta: standard deviation of jump
    M: number of time steps
    I: number paths. '''
    dt = T / M
    rj = lamb * (exp(mu + 0.5 * delta ** 2) - 1)
    S = zeros((I, M + 1), 'd' )
    S[:, 0] = S0
    rand1 = standard_normal ((I, M + 1))
    rand2 = standard_normal ((I, M + 1))
    rand3 = poisson(lamb * dt , (I, M + 1))
    for i in range(1, M + 1, 1):
        if disc == 1:
            S[:, i] = S[:, i - 1] * ((1 + (r - rj) * dt) + sigma
                                * sqrt(dt) * rand1[:, i]
                                + (exp(mu + delta * rand2[:, i]) - 1)
                                * rand3[:, i])
        else:
            S[:, i] = S[:, i - 1] * (exp((r - rj - 0.5 * sigma ** 2) * dt
                                + sigma * sqrt(dt) * rand1[:, i])
                                + (exp(mu + delta * rand2[:, i]) - 1)
                                * rand3[:, i])
    return S     

# Optimal Parameters from Short Calibration
sigma , lamb , mu , delta = [4.94831965e-01, 5.41429261e-01, -9.05877152e+00, 0.]

S = M76_Simulation(S0, T, r, sigma, lamb, mu, delta, M, I)


def M76_Value_Call_MCS(K):
    '''Function to Calculate the MCS Estimator Given K.'''
    return exp(-r * T) * sum(maximum(S[:, M] - K, 0)) / I

print "Value of Call Option %8.3f" % M76_Value_Call_MCS(S0)

# Value Comparisons
strikes = arange(75000 , 92501 , 2500)
values = zeros ((3, len(strikes)), 'd' )
z = 0
for k in strikes:
    print "CALL STRIKE       %10.3f" % k
    print "----------------------------"
    values[0, z] = M76_Value_Call_Int(S0 , k, T, r, sigma ,
                                    lamb , mu , delta)
    print "Call Value by Int %10.3f" % values[0, z]
    
    values[1, z] = M76_Value_Call_FFT(S0 , k, T, r, sigma ,
                                    lamb , mu , delta)
    print "Call Value by FFT %10.3f" % values[1, z]
    print "Difference FFT/Int%10.3f" % (values[1, z] - values[0, z])
    values[2, z] = M76_Value_Call_MCS(k)
    print "Call Value by MCS %10.3f" % values[2, z]
    print "Difference MCS/Int%10.3f" % (values[2, z] - values[0, z])
    print "----------------------------"
    z = z + 1

# Graphical Output
plot(strikes , values[0, :], 'b' )
plot(strikes , values[1, :], 'go' )
plot(strikes , values[2, :], 'rx' )
xlabel( 'Strike' )
ylabel( 'European Call Option Value' )
grid(True)







    
