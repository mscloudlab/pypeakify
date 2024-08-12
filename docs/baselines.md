# Baseline Correction

## Baseline Usage
Baseline correction is a pre-processing technique used to remove the background signal from a spectrum. PyPeakify provides a few options and a simple interface to apply baseline correction to a spectrum. The following baselines are available:
- Identity baseline correction
- Piecewise linear baseline correction
- Cubic spline baseline correction

Baselines are any callable object that takes a `numpy.ndarray` as input from the domain of the spectrum and returns a `numpy.ndarray` of the same shape. Any baseline correction can be pased to the `baseline` parameter of a `Deconvolution` object (see [Deconvolution](deconvolutions.md)).

```python
import numpy as np
... # Other imports
from pypeakify.baseline import PiecewiseLinearBaseline

... # Load a spectrum, initialize peaks

x_nodes = np.array([1600, 1700])
y_nodes = np.array([1, 2])

baseline = PiecewiseLinearBaseline(x_nodes, y_nodes)
deconvolution = Deconvolution(peaks, baseline=baseline)
```

::: pypeakify.baseline
    handler: python
    options:
      show_root_heading: true
      show_source: true
