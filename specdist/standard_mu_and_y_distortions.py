from .utils import *



# note on units: 10^26 Jansky = 1 USI
# Here fequency Nu is in Hz as constants are in USI

#Black body spectrum (in MJy/sr)
def B_nu_of_T(NU,T):
    try:
        result = (2.*hplanck/clight**2.)*NU**3./(np.exp(hplanck*NU/kb/T)-1.)*1.e20
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result

#Derivative of black body spectrum (in MJy/sr/K)
def dB_nu_dT_at_T(NU,T):
    try:
        result = B_nu_of_T(NU,T)/T*(hplanck*NU/kb/T)*np.exp(hplanck*NU/kb/T)/(np.exp(hplanck*NU/kb/T)-1.)
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result

#MU distortion
def dS_dMU(NU,T):
    x = (hplanck*NU/kb/T)
    return -T/x*dB_nu_dT_at_T(NU,T)

#Y distortion
def dS_dY(NU,T):
    x = (hplanck*NU/kb/T)
    try:
        result = T*(x/np.tanh(x/2.)-4.)*dB_nu_dT_at_T(NU,T)
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result


def GetMuSpecDistAtTandX(mu,T,X):
    x = np.asarray(X)
    dist = []
    try:
        for xp in x:
            nu = kb*T/hplanck*xp
            dist.append(mu*dS_dMU(nu,T))
    except:
        nu = kb*T/hplanck*x
        dist.append(mu*dS_dMU(nu,T))
    return np.asarray(dist)

def GetMuSpecDistAtTandX_chluba(mu,T,X):
    x = np.asarray(X)
    dist = []
    try:
        for xp in x:
            nu = kb*T/hplanck*xp
            dist.append(mu*(-dS_dMU(nu,T)*xp*(1./beta_mu-1./xp)))
    except:
        nu = kb*T/hplanck*x
        dist.append(mu*(-dS_dMU(nu,T)*x*(1./beta_mu-1./x)))
    return np.asarray(dist)

def GetYSpecDistAtTandX(y,T,X):
    x = np.asarray(X)
    dist = []
    try:
        for xp in x:
            nu = kb*T/hplanck*xp
            dist.append(y*dS_dY(nu,T))
    except:
        nu = kb*T/hplanck*x
        dist.append(y*dS_dY(nu,T))
    return np.asarray(dist)

def G_bb(x):
    try:
        result =  x*np.exp(x)/(np.exp(x)-1.)**2.
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result

def Y_sz(x):
    try:
        result = G_bb(x)*(x*(np.exp(x)+1.)/(np.exp(x)-1.)-4.)
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result

def M(x):
    try:
        result = (x/beta_mu-1.)*np.exp(x)/(np.exp(x)-1.)**2.
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result


def DI_normalization_in_MJy_per_sr(x,cosmo):
    nu_in_Hz = nu_in_GHz_of_x(x,cosmo)*1e9
    norm_in_MJy_per_sr = 2.*hplanck*nu_in_Hz**3./clight**2.*1e20
    return norm_in_MJy_per_sr

def n_bb(x):
    if x < 1e-3:
        return 1./(x*(1.+x/2.+x**2/6.))
    else:
        return (np.exp(x)-1.)**-1.


def g_nu(nu_in_GHz,Tcmb=2.7255):
    nu_in_Hz = nu_in_GHz*1e9
    x = (hplanck*nu_in_Hz/kb/Tcmb)
    return (x/np.tanh(x/2.)-4.)


def Y_sz_nu_in_GHz(nu_in_GHz,Tcmb=2.7255):
    nu_in_Hz = nu_in_GHz*1e9
    x = (hplanck*nu_in_Hz/kb/Tcmb)
    try:
        result = G_bb(x)*(x*(np.exp(x)+1.)/(np.exp(x)-1.)-4.)
    except RuntimeWarning:
        result = 0.
    if math.isnan(result):
        result = 0.
    return result
