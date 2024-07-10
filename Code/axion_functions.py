import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
import astropy.units as unit
import astropy.constants as const
import itertools

#Define useful functions
def make_hkl(max_h=5,max_k=5,max_l=5, s=False):
    '''This might need to be remade based on what the "primitives" are. Condition is h,k,l must be even.
    F mandates h,k,l share a parity, and S mandates h+k+l is even'''
    full_arr = list(itertools.product(range(max_h), range(max_k), range(max_l)))
    if s:
        filter_func = lambda triple: (triple[0]%2 == triple[1]%2) & (triple[0]%2 == triple[2]%2) & (triple[0]%2 == 0)
        return np.array(list(filter(filter_func, full_arr)))[1:]
    else:
        filter_func = lambda triple: (triple[0]%2 == triple[1]%2) & (triple[0]%2 == triple[2]%2)
        return np.array(list(filter(filter_func, full_arr)))[1:]


def make_hkl_s(max_h=5,max_k=5,max_l=5):
    '''hkl array, where the only condition is h+k+l must be even'''
    full_list = list(itertools.product(range(max_h),range(max_k),range(max_l)))
    filter_func = lambda triple: sum(triple)%2 == 0
    return np.array(list(filter(filter_func, full_list)))[1:] #remove (0,0,0)
    

def mod2(vec3):
    '''Returns the dimensionless magnitude of an array of vectors in the (h,k,l) basis. Factor of 2pi/a has to be multiplied manually'''
    return 3*(vec3[:,0]**2 + vec3[:,1]**2 + vec3[:,2]**2) - 2*(vec3[:,0]*vec3[:,1] + vec3[:,1]*vec3[:,2] + vec3[:,2]*vec3[:,0])

def gdotk(hkl_arr):
    '''Returns gHAT dot kHAT, assuming kHat is in the cartesian x direction'''
    return (-hkl_arr[:,0]+hkl_arr[:,1]+hkl_arr[:,2])/np.sqrt(mod2(hkl_arr))

def w_func(Ea, dVector = False, Delta=1.5, E1=1, E2=6):
    '''Returns array of W(Ea, Delta, E1, E2) where everything is in keV. Infinite Ea is dealt with'''
    w_list = []
    if dVector:
        entangle = np.dstack((Ea, Delta))
        for index in range(entangle.shape[1]):
            E = entangle[0,index,0]
            D = entangle[0,index,1]
            if np.isinf(E) or E<0:
                w_list.append(0)
            else:
                w = (1/2)*(erf((E-E1)/(np.sqrt(2)*D)) - erf((E-E2)/(np.sqrt(2)*D)))
                w_list.append(w)
    else:
        for E in Ea:
            if np.isinf(E) or E<0:
                w_list.append(0)
            else:
                w = (1/2)*(erf((E-E1)/(np.sqrt(2)*Delta)) - erf((E-E2)/(np.sqrt(2)*Delta)))
                w_list.append(w)
    return np.array(w_list)

def FA_q(q2, Z=51):
    '''Returns form factor given an input in AA^(-2)'''
    qme = q2/0.1308
    A = 184.15*np.exp(-1/2)*Z**(-1/3)
    return Z*A**2*qme/(1+A**2*qme)

def make_delta(energy):
    '''Returns Delta (approx 15%*sqrt(E)*E) for an energy array, setting infinities and negatives to zero'''
    output = []
    for E in energy:
        if E<0 or np.isinf(E):
            output.append(0)
        else:
            output.append(0.15463505424062166*np.sqrt(E/1000)*E)
    return np.array(output)

def hkl_to_cart(hkl_array):
    '''Converts from hkl basis to cartesian basis, ignoring factor of 2pi/a'''
    x_axis = - hkl_array[:,0] + hkl_array[:,1] + hkl_array[:,2] 
    y_axis =   hkl_array[:,0] - hkl_array[:,1] + hkl_array[:,2] 
    z_axis =   hkl_array[:,0] + hkl_array[:,1] - hkl_array[:,2] 
    return np.stack((x_axis, y_axis, z_axis), axis=1)

def cart_mag(vec):
    '''Returns cartesian magnitude of a 1d n-vector'''
    return np.sqrt(np.sum(vec**2))

def gdotk_cart(g_arr, k_vec):
    '''Cartesian dot product for 2d array g_arr and 1d 3-vector k_vec. Does not convert to unit vectors'''
    output_list = []
    for g_vec in g_arr:
        output_list.append(g_vec[0]*k_vec[0] + g_vec[1]*k_vec[1] + g_vec[2]*k_vec[2])
    return np.array(output_list)

def make_dpde(Energy_array, coupling = 2e-10):
    '''Creates dPhi/dE for the parametrised blackbody-like form appearing in older papers. Assumes no axion mass.
    Units of cm^(-2) s^(-1) keV^(-1)''' #g_agg (axion-photon-photon) coupling constant; in GeV^(-1) (for photon coalescence)
    #Upper bound on g_ag of 2.7e-10 from the Sun, see Di Luzio's review
    lmda = (coupling/(1e-8))**4
    phi_0 = 5.95e14 #in cm^(-2) s^(-1)
    E_0    = 1.103 #in keV
    dpdt_list = []
    for E in Energy_array:
        if np.isinf(E):
            dpdt_list.append(0)
        else:
            dpdt_list.append(np.sqrt(lmda)*(phi_0)/(E_0) * (E/E_0)**3/(np.exp(E/E_0)-1))
    return np.array(dpdt_list)

def k_from_polar(theta,phi):
    return np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])

