from numpy import *
from matplotlib.pyplot import *
from scipy.interpolate import *
from scipy.optimize import fmin

T = array((1 / 365., 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0))
Y = array((0.0012, 0.0052, 0.0096, 0.0136, 0.0173, 0.0208,
0.0239 , 0.0267 , 0.0290 , 0.0308 , 0.0322))

tck = splrep(T, Y, k=3) # Cubic Splines
step = 10.0 / 20
Tnew = arange(0.0, 10.0 + step , step)
Ycur = splev(Tnew , tck , der=0)
Yder = splev(Tnew , tck , der=1)

figure ()
plot(T, Y, 'ro' )
plot(Tnew , Ycur , 'b' ) # cubic splines
plot(Tnew , Yder , 'g' ) # first derivative
xlabel('Maturity in Years')
ylabel('German Bund yield' )
grid(True)

f = zeros(len(Ycur), float )
for t in range(len(Tnew)):
    f[t] = Ycur[t] + Yder[t] * Tnew[t]
    # forward rate transformation


r0 = 0.0012 # base rate ECB
kappa_r = 2.0
theta_r = 0.04
sigma_r = 0.2
opt1 = [kappa_r , theta_r , sigma_r] # initial guess
if 2 * kappa_r * theta_r < sigma_r ** 2:
    print "Not valid."

def CIR_Error(opt):
    "Error Function for CIR85 Model Calibration."
    kappa_r , theta_r , sigma_r = opt
    fCIR = f_CIR(opt)
    MSE = sum((f - fCIR) ** 2) / len(f)
    if 2 * kappa_r * theta_r < sigma_r ** 2:
        MSE = MSE + 100 # penalty
    elif sigma_r < 0:
        MSE = MSE + 100
    print opt , MSE
    return MSE

# Calibration Procedure
opt = fmin(CIR_Error , opt1 ,
xtol=0.00001 , ftol=0.00001 ,
maxiter=300 , maxfun=500)

fCIR = f_CIR(opt)
error = sum(abs(f - fCIR))
print "Sum Absolute Error %f" % error
print "Av. Absolute Error %f" % (error / len(Tnew))

figure ()
subplot(211)
grid(True)
xlabel('T')
ylabel('f(0,T)')
plot(Tnew , f, 'b' )
plot(Tnew , fCIR , 'ro' )
axis ([min(Tnew) - 0.5, max(Tnew) + 0.5,
    min(fCIR) - 0.005 , max(fCIR) * 1.1])
subplot(212)
grid(True)
wi = 0.3
bar(Tnew - wi / 2, f - fCIR , width=wi)
ylabel('Difference')
axis ([min(Tnew) - 0.5, max(Tnew) + 0.5,
    min(f - fCIR) * 1.1, max(f - fCIR) * 1.1])

