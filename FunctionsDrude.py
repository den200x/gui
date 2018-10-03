import numpy as np

def eq_eU(w, param, mod = False): #Drude - Lorentz model equation @ UV
    '''
    Calculation of the electron Lorentz behavior in the UV range.
    Modify input parameters.
    '''
    [de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D] = param
    if w0_U == 0 and wp_U == 0 and gamma_U == 0:
        return 0
    if mod:
        if w <= (w0_U - gamma_U):
            eU = eq_eU(w, param)
        elif w < w0_U:
            eU = np.real(eq_eU(w0_U - gamma_U, param)) + 1j*np.imag(eq_eU(w, param))
        elif w >= w0_U:
            eq = eq_eU(w0_U, param)
            eU = np.real(eq) + 1j*np.imag(eq)
    else:
        #Divided by 0. Include try / exception and error message if occured.
        eU = wp_U**2/(w0_U**2 - w**2 + 1j* gamma_U * w)
    return eU
 
def eq_eD(w, param, mod = False):
    '''
    Calculation of the electron Lorentz behavior for the valence / conduction electrons.
    Modify input parameters.
    '''
    [de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D] = param
    if mod:
        if w <= (w0_U - gamma_U):
            eD = eq_eD(w, param, False)
        elif w < w0_U:
            eD = np.real(eq_eD(w0_U - gamma_U, param, False)) + 1j*np.imag(eq_eD(w, param, False))
        elif w >= w0_U:
            eD = np.real(eq_eD(w, param, False)) + 1j*np.imag(eq_eD(w, param, False))
    else:
        eD = wp_D**2/(w0_D**2 - w**2 + 1j* gamma_D * w)
    return eD

def e_eq(w, param, mod = False):
    '''
    Equation to calculate complex dieclectric function of a material. The mod parameter determines whether 
    materials on the high frequency side of the UV Lorentz tail is modified. This is relevant for e.g. copper
    where the UV resonance frequency is in the visible spectrum.
    '''
    de = param[0]
    return de + eq_eU(w, param, mod) + eq_eD(w, param)

def leastsq_function(x, param, scale):
    '''
    Returns fit results using magnitude and phase. Not used.
    '''
    n = int(len(x) / 2)
    yfit = np.empty(len(x))
    yfit[:n] = lorentzMag_function(x[:n],param)
    yfit[n:] = np.multiply(lorentzPhase_function(x[n:], param),scale)
    return yfit

#Lorentz function converted to magnitude
def lorentzMag_function(x, param):
    [de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D] = param
    result = de + wp_U**2/(w0_U**2 - x**2 + 1j* gamma_U * x) + wp_D**2/(w0_D**2 - x**2 + 1j* gamma_D * x)
    real = np.real(result)
    imag = np.imag(result)
    return mag(real, imag)

 #Lorentz function converted to phase
def lorentzPhase_function(x, param):
    [de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D] = param
    result = de + wp_U**2/(w0_U**2 - x**2 + 1j* gamma_U * x) + wp_D**2/(w0_D**2 - x**2 + 1j* gamma_D * x)
    return phase(np.real(result), np.imag(result))

def leastsq_functionNK(x, de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D):
    n = int(len(x) / 2)
    yfit = np.empty(len(x))
    param = [de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D]
    #yfit[:n] = N_function(x[:n], param)
    #yfit[n:] = K_function(x[n:], param)
    yfit[:] = NandK_function(x[:n], param) # this function achieves the same as above two lines but faster
    return yfit

def N_function(x, param):
    #z = de + wp_U**2/(w0_U**2 - x**2 + 1j* gamma_U * x) + wp_D**2/(w0_D**2 - x**2 + 1j* gamma_D * x)
    π = np.pi
    c = 299792458.0 #unit: m/s,speed of light
    y = []
    for wvl in x:
        w = 2*π * c * 10**9 / wvl
        z = e_eq(w, param, True)
        real = np.real(z)
        imag = np.imag(z)
        y.append(1/2**0.5 * (real + (real**2 + imag**2)**0.5)**0.5)
    return y
    #return np.multiply(1/2**0.5, np.sqrt(np.add(real, np.sqrt(np.power(real,2) + np.power(imag,2)))))
    
def K_function(x, param):
    #[de, w0_U, wp_U,gamma_U, w0_D, wp_D,gamma_D] = param
    #z = de + wp_U**2/(w0_U**2 - x**2 + 1j* gamma_U * x) + wp_D**2/(w0_D**2 - x**2 + 1j* gamma_D * x)
    π = np.pi
    c = 299792458.0 #unit: m/s,speed of light
    y = []
    for wvl in x:
        w = 2*π * c * 10**9 / wvl
        z = e_eq(w, param, True)
        real = np.real(z)
        imag = np.imag(z)
        y.append(-1/2**0.5 * (-real + (real**2 + imag**2)**0.5)**0.5)
    return y
    #return np.multiply(-1/2**0.5, np.sqrt(np.subtract(np.sqrt(np.power(real,2) + np.power(imag,2)), real)))

def NandK_function(x, param):
    n = np.array([])
    k = np.array([])
    π = np.pi
    c = 299792458.0 #unit: m/s,speed of light
    for wvl in x:
        w = 2*π * c * 10**9 / wvl
        z = e_eq(w, param, True)
        real = np.real(z)
        imag = np.imag(z)
        n = np.append(n, 1/2**0.5 * (real + (real**2 + imag**2)**0.5)**0.5)        
        k = np.append(k, -1/2**0.5 * (-real + (real**2 + imag**2)**0.5)**0.5)
    #return np.concatenate((Y1, Y2), axis=0)
    return (n, k) 

def mag(Real, Imag):
    return ((Real - 1)**2 + Imag**2)**0.5
        
def phase(Real, Imag):
    return np.arctan(Imag/(Real-1))

