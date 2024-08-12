# Peaks

<!-- PyPeakify is inherently object-oriented, and the `Peak` class is the primary object used to represent peaks in spectra. -->

## Overview

PyPeakify currently supports two primary peak types, Gaussians and Lorentzians. The peak type can be chosen in the constructor, or changed at any time by changing the `peak_type`.

Additionally, you can provide optimization constraints directly to the peak objects themselves by modifying the `constrain_X` attributes, where `X` is in the set {`width`, `amplitude`, `position`}. These constraints are respected by the optimization algorithm when fitting the peaks to a spectrum, and are not asserted if parameters are modified outside of that context.

```python
from pypeakify.peak import Peak

# Create a Gaussian peak
gaussian_peak = Peak(peak_type='gaussian', width=1.0, amplitude=1.0, position=0.0)

# Create a Lorentzian peak
lorentzian_peak = Peak(peak_type='lorentzian', width=1.0, amplitude=1.0, position=0.0)
```

::: pypeakify.peak
    handler: python
    options:
      show_root_heading: true
      show_source: true

