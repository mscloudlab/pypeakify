import numpy as np
import copy
from scipy.optimize import curve_fit
from tabulate import tabulate

from .peak import gaussian, lorentzian, Peak
from .baseline import IdentityBaseline

class Deconvolution:
    '''
    A class representing a deconvolution of a spectrum.
    '''
    
    def __init__(self, peaks, baseline=IdentityBaseline()):
        '''
        Constructor for the Deconvolution class.
        
        Args:
            peaks (list): List of Peak objects to be fit to the spectrum.
            baseline (Baseline): Baseline for fitting peaks. Default is the identity baseline.
        '''
        self.peaks = [copy.deepcopy(peak) for peak in peaks]
        self.baseline = baseline
        
        self.N = len(peaks)
    
    def fit(self, x, y):
        '''
        Fits the peaks to the spectrum.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the spectrum.
            y (numpy.ndarray): y-values of the spectrum.
        '''
        base = self.baseline(x)
        
        # rescale so numerically feasible
        scale_x = np.max(x) - np.min(x)
        
        fit_params = np.zeros(3*self.N)
        min_bounds = np.zeros_like(fit_params)
        max_bounds = np.zeros_like(fit_params)
        
        for i, peak in enumerate(self.peaks):
            fit_params[3*i:3*i+3] = [peak.width / scale_x, peak.amplitude, peak.position / scale_x]
            
            min_bounds[3*i:3*i+3] = [peak.constrain_width[0] / scale_x, peak.constrain_amplitude[0], peak.constrain_position[0] / scale_x]
            max_bounds[3*i:3*i+3] = [peak.constrain_width[1] / scale_x, peak.constrain_amplitude[1], peak.constrain_position[1] / scale_x]

        def optim_func(x0, *params):
            '''
            Function to be minimized in the optimization process.
            
            Args:
                x (numpy.ndarray): x-values at which to evaluate the function.
                *params: Parameters to be optimized.
            '''
            y0 = np.zeros_like(x)
            for i in range(0, len(params), 3):
                peak = Peak(self.peaks[int(i // 3)].peak_type, *params[i:i+3])
                y0 += peak(x0)
            return y0

        self.fit_params, self.pcov = curve_fit(optim_func, x / scale_x, y - base, p0=fit_params, bounds=(min_bounds, max_bounds), maxfev=100000)
        self.perr = np.sqrt(np.diag(self.pcov))
        
        for i in range(self.N):
            self.peaks[i].width, self.peaks[i].amplitude, self.peaks[i].position = self.fit_params[3*i:3*i+3]
            
            fp = self.fit_params[3*i:3*i+3]
            
            self.peaks[i].width *= scale_x
            self.peaks[i].position *= scale_x
            
            perr = self.perr[3*i:3*i+3]
            
            self.peaks[i].set_perr(perr[0] * scale_x, perr[1], perr[2] * scale_x)
        
        print(self)
    
    def __str__(self):
        '''
        Returns a string representation of the deconvolution.
        '''
        return tabulate(
            [[peak.peak_type, peak.width, peak.amplitude, peak.position] for peak in self.peaks],
            headers=['Peak Type', 'Width', 'Amplitude', 'Position']
        )

    def __call__(self, x):
        '''
        Calculates the value of the deconvolution at the given x-values.
        
        Args:
            x (numpy.ndarray): x-values at which to evaluate the deconvolution.
        '''
        y = np.zeros_like(x)
        for i in range(0, self.N*3, 3):
            y += self.peaks[int(i // 3)](x)
        return y

    def plot(self, ax, x, y=None, show_base=True, show_peaks=True, show_error=False, **kwargs):
        '''
        Plots the deconvolution on the given axis.
        
        Args:
            ax (matplotlib.axes.Axes): Axis on which to plot the deconvolution.
            x (numpy.ndarray): x-values at which to evaluate the deconvolution.
            y (numpy.ndarray): y-values of the ground truth spectrum. Optional.
            show_base (bool): Whether or not to plot the baseline.
            show_peaks (bool): Whether or not to plot the individual peaks.
            show_error (bool): Whether or not to plot the error bars.
            **kwargs: Additional matplotlib keyword arguments to be passed to the plot.
        '''
        if show_peaks:
            for peak in self.peaks:
                peak.plot(ax, x, baseline=self.baseline if show_base else None, show_error=show_error, color='r', ls='--', **kwargs)
                
        y_pred = self(x)
        if show_base:
            y_pred += self.baseline(x)
        ax.plot(x, y_pred, c='b', ls='--', label='Deconvolution', **kwargs)
        
        if y is not None:
            ax.plot(x, y, label='Ground Truth', c='k')
        