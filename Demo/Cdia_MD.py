import numpy as np
from ase import Atoms
from ase.calculators.emt import EMT
from deepmd.calculator import DP
from ase import units
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.io import write,Trajectory
from ase.md import MDLogger
from ase.build import bulk
from ase.io import write

label=3
file_name="Cdia"
atoms = bulk(name="C", crystalstructure="diamond", a=3.56).repeat((2,2,2))
# atoms=Diamond(size=(2,2,2), symbol='C', pbc=(1,1,1))

write(f"{file_name}.png",atoms,rotation="30x,30y,30z")

atoms.set_calculator(DP(model=f"{label}1.train/graph.pb"))

dt = 1 * units.fs
temp0, nsteps0 = 600, 200
taut = 20*units.fs

MaxwellBoltzmannDistribution(atoms, temp0*units.kB)
dyn = NVTBerendsen(atoms, dt, temp0, taut=taut, trajectory=f'traj/{file_name}.traj')
def myprint():
    print(f'time={dyn.get_time() / units.fs: 5.0f} fs ' + \
          f'T={atoms.get_temperature(): 3.0f} K')
dyn.attach(myprint, interval=20)
dyn.attach(MDLogger(dyn, atoms, f"log/{file_name}.log", header=True, peratom=True, mode="w"), interval=10)
dyn.run(nsteps0)

temps=[620,630,640,650,660]
for i,temp in enumerate(temps):
      dyn.set_temperature(temp)
      dyn.run(200)

traj=Trajectory(f"traj/{file_name}.traj")
write(f"gif/{file_name}.gif", traj[::10], rotation="30x,30y,30z")
# atoms=Atoms(
#       "C16",
#       positions=[
#         (0.0000, 0.0000, 0.0000),
#         (0.8900, 0.8900, 0.8900),
#         (0.0000, 1.7800, 1.7800),
#         (0.8900, 2.6700, 2.6700),
#         (1.7800, 0.0000, 1.7800),
#         (2.6700, 0.8900, 2.6700),
#         (1.7800, 1.7800, 3.5600),
#         (2.6700, 2.6700, 4.4500),
#         (1.7800, 1.7800, 0.0000),
#         (2.6700, 2.6700, 0.8900),
#         (1.7800, 3.5600, 1.7800),
#         (2.6700, 4.4500, 2.6700),
#         (3.5600, 1.7800, 1.7800),
#         (4.4500, 2.6700, 2.6700),
#         (3.5600, 3.5600, 3.5600),
#         (4.4500, 4.4500, 4.4500)
#       ],
#       cell=[
#        (-3.5600, 0.0000,3.5600),
#        ( 0.0000,3.5600,3.5600),  
#        (-3.5600, 3.5600,0.0000)
#       ],
# )

# write(f"img/{prefix}.png", atoms, rotation="30x, 30y, 30z")

# # choose model
# # atoms.set_calculator(EMT())
# atoms.set_calculator(DP(model=f"{label}1.train/graph.pb"))

# dt = 1 * units.fs
# temp0, nsteps0 = 300, 200
# temp1, nsteps1 = 300, 400
# taut = 10*units.fs
# num_interval=10

# MaxwellBoltzmannDistribution(atoms, temp0*units.kB)
# dyn = NVTBerendsen(atoms, dt, temp0, taut=taut, trajectory=f'traj/{prefix}.traj')


# ## case of C16
# def myprint():
#     print(f'time={dyn.get_time() / units.fs: 5.0f} fs '+f'T={atoms.get_temperature(): 3.0f} K')


# ### common
# dyn.attach(myprint, interval=10)
# dyn.attach(MDLogger(dyn, atoms, f"log/{prefix}.log", header=True, peratom=True, mode="w"), interval=num_interval)

# dyn.run(nsteps0)
# dyn.set_temperature(temp1)
# dyn.run(nsteps1)

# traj=Trajectory(f"traj/{prefix}.traj")
# write(f"gif/{prefix}.gif", traj[::10], rotation="30x,30y,30z")