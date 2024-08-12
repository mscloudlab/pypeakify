__version__ = "1.0.1"

from .peak import Peak, gaussian, lorentzian
from .deconvolution import Deconvolution
from .baseline import PiecewiseLinearBaseline, IdentityBaseline, CubicSplineBaseline
from .filereader import import_ascii_file, import_ascii_url, crop, normalize_data, nearest_points

from . import baseline
from . import deconvolution
from . import filereader
from . import peak
