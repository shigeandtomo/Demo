# Demo

Original dpdata is found [here](https://github.com/deepmodeling/dpdata/tree/master).

## How to use

### sample files description

1. `00.data` CH4 with ABACUS (, CP2K, or VASP)
1. `10.data` CH4 with OpenMX
1. `20.data` H2O with OpenMX

Each folder named `train` contains `input.json`, deepmd-kit input script.
```
# import os
# os.chdir("work")
# ! git clone https://github.com/deepmodeling/dpdata tmp
# ! cp -r tmp/dpdata .
! cp -r openmx dpdata/
! cp openmx.py dpdata/plugins/
```
## Import libraries
Now, we can use deepmd with OpenMX. Then, import following libraries.
```
import os
import dpdata
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ang2bohr = 1.88972612463
bohr2ang = 0.529177210903
```
#### Note: Even if "dpdata" has already been installed, the package named "dpdata" in the current directory is imported first.