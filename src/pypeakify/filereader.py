import csv
import requests
import numpy as np
import jcamp

def import_ascii_file(fname, delim=None):
    '''
    Import x (abscissa), y (ordinate) spectrum data from file. Assumes two column ascii format where the first column is x and the second column is y.
    
    Args:
        fname (str): Path to file.
        delim (str): Delimiter used in file. If None, will attempt to guess.
    '''
    try:
        f = open(fname, 'r')
    except IOError:
        print(f'Unable to open file at {fname}')
        return None, None
    except Exception as e:
        print(f'Error: {e}')
        return None, None
    else:
        with f:
            fc = f.read()
            if delim is None:
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(fc).delimiter
                x, y = np.transpose(np.genfromtxt(fc.splitlines(), delimiter=delimiter))
            else:
                x, y = np.transpose(np.genfromtxt(fc.splitlines(), delimiter=delim))
            
            if x is None or y is None:
                print(f'Error: Unable to parse data from {fname}')
                return None, None

            # sort y w.r.t. x
            x_ind = np.argsort(x)
            x, y = x[x_ind], y[x_ind]
            return x, y

def import_jcamp_file(fname):
    '''
    Import spectrum data from JCAMP file.
    
    !!! note
        JCAMP-DX files are loaded using the [`jcamp`](https://pypi.org/project/jcamp/) package.
        Unlike ASCII files which are assumed to have a single spectrum, JCAMP files can contain multiple spectra, and should be handled accordingly by the user.
    
    Args:
        fname (str): Path to file.
    '''
    return jcamp.jcamp_readfile(fname)

def import_ascii_url(url, delim=None):
    '''
    Import x (abscissa), y (ordinate) spectrum data from URL. Assumes two column ascii format where the first column is x and the second column is y.
    
    Args:
        url (str): URL to file.
        delim (str): Delimiter used in file. If None, will attempt to guess.
    '''
    try:
        response = requests.get(url)
        if delim is None:
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(response.text).delimiter
            x, y = np.transpose(np.genfromtxt(response.text.splitlines(), delimiter=delimiter))
        else:
            x, y = np.transpose(np.genfromtxt(response.text.splitlines(), delimiter=delim))

        if x is None or y is None:
            print(f'Error: Unable to parse data from {url}')
            return None, None

        # sort y w.r.t. x
        x_ind = np.argsort(x)
        x, y = x[x_ind], y[x_ind]
        return x, y
    except IOError:
        print(f'Unable to open file at {url}')
        return None, None
    except Exception as e:
        print(f'Error: {e}')
        return None, None

def import_jcamp_url(url):
    '''
    Import spectrum data from JCAMP file at URL.
    
    !!! note
        JCAMP-DX files are loaded using the [`jcamp`](https://pypi.org/project/jcamp/) package.
        Unlike ASCII files which are assumed to have a single spectrum, JCAMP files can contain multiple spectra, and should be handled accordingly by the user.
    
    Args:
        url (str): URL to file.
    '''
    try:
        response = requests.get(url)
        return jcamp.jcamp_readfile(response.text)
    except IOError:
        print(f'Unable to open file at {url}')
        return None
    except Exception as e: 
        print(f'Error: {e}')
        return None

def normalize_data(x, y, range=None):
    '''
    Normalize y data to range [0, 1].
    
    If range is not None, normalize y data to range [0, 1] within the specified x range.
    
    x and y must have the same shape.
    
    Args:
        x (np.array): x data.
        y (np.array): y data.
        range (tuple): x range to normalize y data within. If None, normalize y data to range [0, 1].
    '''
    if range is None:
        return x, (y - np.min(y)) / (np.max(y) - np.min(y))
    diffs1 = np.abs(x - range[0])
    diffs2 = np.abs(x - range[1])
    i1 = np.argmin(diffs1)
    i2 = np.argmin(diffs2)
    return x, (y - np.min(y[i1:i2])) / (np.max(y[i1:i2]) - np.min(y[i1:i2]))

def crop(x, y, range):
    '''
    Crop x, y data to specified x range. `range` must be a pair of values in the domain of x.
    
    x and y must have the same shape.
    
    Args:
        x (np.array): x data.
        y (np.array): y data.
        range (tuple): x range to crop x, y data to, in the form (x_min, x_max).
    '''
    diffs1 = np.abs(x - range[0])
    diffs2 = np.abs(x - range[1])
    i1 = np.argmin(diffs1)
    i2 = np.argmin(diffs2)
    x = x[i1:i2]
    y = y[i1:i2]
    return x, y

def nearest(x, y, x0):
    '''
    Find the y value in y that corresponds to the nearest x value to x0.
    
    Useful e.g. for identifying nodes for baseline correction that exist on the spectrum.
    
    Args:
        x (np.array): x data.
        y (np.array): y data.
        x0 (float): x value to find nearest y value for.
    '''
    idx = (np.abs(x-x0)).argmin()
    return y[idx]

def nearest_points(x, y, x0):
    '''
    Find the y values in y that correspond to the nearest x values to x0.
    
    Useful e.g. for identifying nodes for baseline correction that exist on the spectrum.
    
    Args:
        x (np.array): x data.
        y (np.array): y data.
        x0 (np.array): x values to find nearest y values for.
    '''
    return np.array([nearest(x, y, x0i) for x0i in x0])

