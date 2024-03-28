# Demonstration

Original dpdata is found [here](https://github.com/deepmodeling/dpdata/tree/master).

## How to prepare

```
git clone -b devel https://github.com/deepmodeling/dpdata && cd dpdata && pip install .
```
(optional)
```
pip install -r requirements.txt
```

## How to use

### sample files description

1. `00.data` CH4 with ABACUS (, CP2K, or VASP)
1. `10.data` CH4 with OpenMX
1. `20.data` H2O with OpenMX

Each folder named `train` contains `input.json`, deepmd-kit input script.

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
