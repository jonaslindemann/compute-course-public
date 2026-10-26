# fstats - a minimal Fortran extension package

An example of how a Fortran module wrapped with f2py can be distributed as a
Python package, using the [meson-python](https://meson-python.readthedocs.io)
build backend.

```
package_example/
├── pyproject.toml     # Package metadata and build backend
├── meson.build        # How to build the extension module
└── src/
    └── fstats.f90     # The Fortran code (module stats)
```

Build and install the package, with a Fortran compiler available:

```
pip install .
```

Use it from Python:

```python
import numpy as np
from fstats import stats

print(stats.normalize(np.array([1.0, 2.0, 3.0, 4.0])))
```

To build a wheel that can be installed on other computers with the same
platform and Python version:

```
pip wheel . --no-deps -w dist
```
