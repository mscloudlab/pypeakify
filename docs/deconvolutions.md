# Deconvolutions

## Overview

The `deconvolutions` module provides functions for deconvolving peaks from a spectrum. It establishes a least squares optimization problem to fit a sum of peaks to a spectrum, and provides a simple interface for solving this problem.

## Deconvolution Usage

Once baseline and peak objects have been initialized, a `Deconvolution` object can be created to fit the peaks to the spectrum.

When fit, a deconvolution object modifies *copies* of the peak objects to fit the spectrum. The original peak objects are not modified, and can be used for other deconvolutions. If a deconvolution object is refit to a different spectrum, the current state of the peaks will be used as the initial guess in the optimization problem.

As a useful utility, when the object is printed, the fitted peak parameters are displayed in table form using the `tabulate` package.

```python
import numpy as np
... # Other imports
from pypeakify.deconvolution import Deconvolution

... # Load a spectrum, initialize peaks and baseline
deconvolution = Deconvolution(peaks, baseline=baseline)
deconvolution.fit(spectrum)

print('Fitted peaks:')
print(deconvolution)
```

::: pypeakify.deconvolution
    handler: python
    options:
      show_root_heading: true
      show_source: true
