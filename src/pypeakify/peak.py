import numpy as np

def gaussian(x, width, amplitude, position):
    '''
    Calculates the value of a Gaussian peak at the given x-values.
    
    Args:
        x (numpy.ndarray): x-values at which to evaluate the peak.
        width (float): Width of the peak.
        amplitude (float): Amplitude of the peak.
        position (float): Position of the peak.
    '''
    return amplitude * np.exp(-0.5 * ((x - position) / width)**2)

def lorentzian(x, width, amplitude, position):
    '''
    Calculates the value of a Lorentzian peak at the given x-values.
    
    Args:
        x (numpy.ndarray): x-values at which to evaluate the peak.
        width (float): Width of the peak.
        amplitude (float): Amplitude of the peak.
        position (float): Position of the peak.
    '''
    return amplitude / (1 + ((x - position) / width)**2)

class Peak:
    '''
    A class representing a peak in a spectrum.
    
    Notably, the user initializes a peak, and then uses a `Deconvolution` object to fit the peak to a spectrum.
    The peak can be plotted using the `plot` method.
    '''
    
    def __init__(self, peak_type, width, amplitude, position, constrain_width=(0,np.inf), constrain_amplitude=(0,np.inf), constrain_position=(-np.inf,np.inf)):
        '''
        Constructor for the Peak class.
        
        Args:
            peak_type (str): Type of peak to be used. Of 'gaussian' or 'lorentzian'.
            width (float): Initial width of the peak.
            amplitude (float): Initial amplitude of the peak.
            position (float): Initial position of the peak.
            constrain_width (tuple): Tuple of the form (min, max); range for the width of the peak.
            constrain_amplitude (tuple): Tuple of the form (min, max); range for the amplitude of the peak.
            constrain_position (tuple): Tuple of the form (min, max); range for the position of the peak.
        '''
        
        assert peak_type in ['gaussian', 'lorentzian'], "peak_type must be 'gaussian' or 'lorentzian'."
        
        self.peak_type = peak_type
        self.width = width
        self.amplitude = amplitude
        self.position = position
        self.constrain_width = constrain_width
        self.constrain_amplitude = constrain_amplitude
        self.constrain_position = constrain_position
    
    def __call__(self, x):
        '''
        Calculates the value of the peak at the given x-values.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the peak.
        '''
        if self.peak_type == 'gaussian':
            return gaussian(x, self.width, self.amplitude, self.position)
        elif self.peak_type == 'lorentzian':
            return lorentzian(x, self.width, self.amplitude, self.position)
        else:
            raise ValueError("`peak_type` must be 'gaussian' or 'lorentzian'.")
    
    def set_perr(self, width_perr, amplitude_perr, position_perr):
        self.width_perr = width_perr
        self.amplitude_perr = amplitude_perr
        self.position_perr = position_perr
    
    def get_fit_error(self, x):
        '''
        Calculates the error bars of the peak at the given x-values given 1-sigma from the fit, as set by `set_perr`.
        
        Returns a pair of the upper (`ub`) and lower (`lb`) bounds of the peak where `ub` and `lb` are the same shape as `x`.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the peak.
        '''
        if self.peak_type == 'gaussian':
            ub = gaussian(x, self.width + self.width_perr, self.amplitude + self.amplitude_perr, self.position + self.position_perr)
            lb = gaussian(x, self.width - self.width_perr, self.amplitude - self.amplitude_perr, self.position - self.position_perr)
            return ub, lb
        elif self.peak_type == 'lorentzian':
            ub = lorentzian(x, self.width + self.width_perr, self.amplitude + self.amplitude_perr, self.position + self.position_perr)
            lb = lorentzian(x, self.width - self.width_perr, self.amplitude - self.amplitude_perr, self.position - self.position_perr)
            return ub, lb
        else:
            raise ValueError("`peak_type` must be 'gaussian' or 'lorentzian'.")

    def plot(self, ax, x=None, baseline=None, show_error=False, **kwargs):
        '''
        Plots the peak on the given axis.
        
        Args:
            ax (matplotlib.axes.Axes): Axis on which to plot the peak.
            x (numpy.ndarray): x-values at which to evaluate the peak. If None, x-values are generated near the position.
            baseline (Baseline): Baseline object to be plotted along with the peak. If None, no baseline is plotted.
            show_error (bool): Whether or not to plot error bars on the peak.
            **kwargs: Additional matplotlib keyword arguments to be passed to the plot function.
        '''
        if x is None:
            fwhm = self.get_fwhm()
            x = np.linspace(self.position - 4*fwhm, self.position + 4*fwhm, 1000)
        
        if show_error:
            ub, lb = self.get_fit_error(x)
            if baseline is not None:
                ub += baseline(x)
                lb += baseline(x)
            ax.fill_between(x, lb, ub, alpha=0.5, **kwargs)
        
        y = self(x)
        if baseline is not None:
            y += baseline(x)
        ax.plot(x, y, **kwargs)
        
    def get_fwhm(self):
        '''
        Gets the full width at half maximum of the peak.
        '''
        if self.peak_type == 'gaussian':
            # 2 sqrt(2 ln(2)) ~= 2.35482005
            return 2.35482005 * self.width
        elif self.peak_type == 'lorentzian':
            return 2 * self.width
        else:
            raise ValueError("peak_type must be 'gaussian' or 'lorentzian'.")
