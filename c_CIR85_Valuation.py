#
# Valuation of Zero -Coupon Bonds in CIR85 Model
# Model Parameters from Calibration
# to German Bund Yield Curve (22. April 2010)
# c_CIR85_Valuation.py
#
# (c) Dr. Yves J. Hilpisch
# Script for illustration purposes only.
#
from numpy import *
from matplotlib.pyplot import *
from b_CIR85_Cal_Results import *



#
# Example Parameters
#
t = 0.5
T = 10.0

#
# Zero -Coupon Bond Valuation Formula
#

def gamma(kappa_r , sigma_r):
    'Help Function.'
    return sqrt(kappa_r ** 2 + 2 * sigma_r ** 2)

def b1(alpha):
    'Help Function.'
    r0 , kappa_r , theta_r , sigma_r , t, T = alpha
    g = gamma(kappa_r, sigma_r)
    return (((2 * g * exp(( kappa_r + g) * (T - t) / 2)) /
            (2 * g + (kappa_r + g) * (exp(g * (T - t)) - 1)))
            ** (2 * kappa_r * theta_r / sigma_r ** 2))

def b2(alpha):
    'Help Function.'
    r0 , kappa_r , theta_r , sigma_r , t, T = alpha
    g = gamma(kappa_r, sigma_r)
    return ((2 * (exp(g * (T - t)) - 1)) /
            (2 * g + (kappa_r + g) * (exp(g * (T - t)) - 1)))

def B(alpha):
    '''Function to Value Unit Zero -Coupon Bonds in CIR85 Model.
    kappa_r: mean -reversion factor
    theta_r: long -run mean of short rate
    sigma_r: volatility of short rate
    r0: initial short rate
    t: valuation date
    T: final date'''
    b_1 = b1(alpha)
    b_2 = b2(alpha)
    r0 , kappa_r , theta_r , sigma_r , t, T = alpha
    Ert = theta_r + exp(-kappa_r * t) * (r0 - theta_r)
        # expected value of r_t
    return b_1 * exp(-b_2 * Ert)


#
# Example Valuation
#
alpha = [r0 , kappa_r , theta_r , sigma_r , t, T]
BtT = B(alpha)
    # discount factor , ZCB value
print "ZCB Value %10.4f" % BtT

#
# Graphical Output
#
timL = arange(0.0, 10.5, 0.5)
comp = zeros ((len(timL)), 'f' )

for t in timL:
    j = searchsorted(timL, t)
    alpha = [r0 , kappa_r , theta_r , sigma_r , t, T]
    comp[j] = B(alpha)

plot(timL , comp , 'b' )
plot(timL , comp , 'ro' )
xlabel( 'Years' )
ylabel( 'Bond Value' )
grid(True)








