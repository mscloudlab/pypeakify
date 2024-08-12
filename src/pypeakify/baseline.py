import numpy as np
from scipy.interpolate import CubicSpline

class IdentityBaseline:
    '''
    No baseline correction, or the identity baseline
    '''
    def __init__(self):
        pass
    
    def __call__(self, x):
        '''
        Calculates the value of the baseline at the given x-values.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the baseline.
        '''
        return np.zeros_like(x)

class CubicSplineBaseline:
    '''
    Baseline represented by a cubic spline.
    '''
    def __init__(self, x, y, bc_type='not-a-knot'):
        '''
        Constructor for the cubic spline baseline.
        
        Args:
            x (numpy.ndarray): x-values of the cubic spline.
            y (numpy.ndarray): y-values of the cubic spline.
            bc_type (str): Type of boundary condition to use. Default is 'not-a-knot'. See `scipy.interpolate.CubicSpline` for more information.
        '''
        self.spline = CubicSpline(x, y)
    
    def __call__(self, x):
        '''
        Calculates the value of the baseline at the given x-values.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the baseline.
        '''
        return self.spline(x)

class PiecewiseLinearBaseline:
    '''
    Baseline represented by a piecewise linear function.
    '''
    def __init__(self, x, y):
        '''
        Constructor for the piecewise linear baseline. 
        
        Any values outside of the range of the provided set of vertices are set to the value at the nearest edge vertex.
        
        Args:
            x (numpy.ndarray): x-values of the vertices of the piecewise linear function
            y (numpy.ndarray): y-values of the vertices of the piecewise linear function
        '''
        self.x = x
        self.y = y
    
    def __call__(self, x):
        '''
        Calculates the value of the baseline at the given x-values.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the baseline.
        '''
        return np.interp(x, self.x, self.y)
        
    
    