"""

@authors:

# =============================================================================
 Information: 

    The functions in this script are used to import and fetch values and arrays 
    from text files
        
# =============================================================================
"""

# =============================================================================
# LIBRARIES
# =============================================================================
import numpy as np
from numpy import pi, sin, cos
from scipy.special import lpmn
import math

#import GH_convert     as conv
#import GH_generate    as gen
#import GH_solve       as solv
#import GH_displayCoef as dcoef
#import GH_displaySat  as dsat
#import GH_export      as exp
#import GH_displayTopo as dtopo
#import GH_terminal    as term

from GH_convert import cart2sphA

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
data_path = "../data"


# =============================================================================
# FUNCTIONS - GEODESY
# =============================================================================
def Get_Radius(angle):
    """
    Returns the radius of the reference elipsoid in meters
    
    Input: 
        angle: latitude, inclination from the z axis in degrees
    Output: 
        R: Radius in meters
        
    """    
    theta = pi/2 -angle
    Radius_eq = 6378137 # m
    Radius_pol = 6356752.3142 # m
    a = Radius_eq
    b = Radius_pol     
    deno = np.sqrt(a**2*sin(theta)**2 + b**2*np.cos(theta)**2)
    R = a*b/deno    
    return R


# =============================================================================
# FUNCTIONS - MATHEMATICAL VALUES
# =============================================================================

def Pol_Legendre (l, m, x):
    """
    returns an array[m+1,n+1] of the values of the associated Legendre function 
    of all integer degrees l and order m, at point x
    """
    Pnm_z, Pnm_dz = lpmn(m, l, x)
    return Pnm_z, Pnm_dz #[m, l]


def Normalize (l, m):
    """
    Returns the normalization coefficient of degree l and order m
    """
    d_om = 0
    if m==0 :
        d_om = 1
        
    P1 = math.factorial(l - m)
    P2 = (2*l + 1)
    P3 = (2 - d_om)
    P4 = math.factorial(l + m)
    
    N = np.sqrt(P1*P2*P3/P4)
    return N    



# =============================================================================
# FUNCTIONS - BASEMAP PARAMETERS
# =============================================================================

def Basemap_Parameters ():
    proj = "mill" # projection
    LatS = -90 # llcrnrlat
    LatN = 90 # urcrnrlat 
    LongW = -180 # llcrnrlon
    LongE = 180 # urcrnrlon
    TS = 20 # lat_ts -- I don't know what this is but everyone online uses it so yeah
    Res = "l" # resolution, Crude, Low, [Intermediate, High, Full] > download extensions
    
    Bm_Param = [proj, LatS, LatN, LongW, LongE, TS, Res]
    return proj, LatS, LatN, LongW, LongE, TS, Res











# =============================================================================
# FUNCTIONS TO FETCH FILES
# =============================================================================
def Fetch_Pos(file_name, days = 0.7):
    """
    Imports coordinates from file_name text file (generated from GMAT)
    
    Input:
        file_name: well, the file's name! remove all header text
        days: what time duration the outplut file should correspond to 
              regardless of the sampling rate
    Output: 
        Pos: The position of the satellite in spherical coordinates
        Time: Associated time sampling of each position
    
    """
    Eph = np.loadtxt(f"{data_path}/{file_name}")
    t = np.array(Eph[:,0]) #time in seconds
    x = np.array(Eph[:,1]) #  \
    y = np.array(Eph[:,2]) #  | cordinates, in km
    z = np.array(Eph[:,3]) # /
    dt = np.int(t[1]*100)/100
    L = np.int(days*(86400/dt))
    # convert coord system and shorten array if needed 
    pts = np.transpose(np.array([x,y,z])) 
    if L >= len(pts):
        L = len(pts)
    Pos = cart2sphA(pts[:L]) 
    Time = t[:L]
    print(f"Importing Pos file with {L} coordinates.")
    return Pos, Time


def Fetch_Coef():
    """
    Returns the spherical harmonic coefficients for Earth's Geoid
    Data originally extracted from : EGM2008_to2190_ZeroTide.txt
    These coefs are already normalized
    These files exist with a degree up to lmax = 2190
    """    
    data_path = "../data"
    HC = np.loadtxt(f"{data_path}/GeoPot_Coef_cos_deg30.txt")
    HS = np.loadtxt(f"{data_path}/GeoPot_Coef_sin_deg30.txt")
    return HC, HS


def Fetch_Topo_Coef():
    """
    Returns the spherical harmonic coefficients for Earth's Topology
    Data originally extracted from : Coeff_Height_and_Depth_to2190_DTM2006.txt
    These coefs are already normalized
    These files exist with a degree up to lmax = 2190
    """    
    data_path = "../data"
    HC_topo = np.loadtxt(f"{data_path}/Height_Coef_cos_deg49.txt")
    HS_topo = np.loadtxt(f"{data_path}/Height_Coef_sin_deg49.txt")
    return HC_topo, HS_topo
# =============================================================================
# TEST FUNCTIONS
# =============================================================================
  
# =============================================================================
# MAIN 
# =============================================================================
if __name__ == '__main__':
#    HC, HS = Fetch_Coef()
    
    print("\nGH_import done")
