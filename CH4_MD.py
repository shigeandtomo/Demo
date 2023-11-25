import numpy as np
from ase import Atoms
from ase.calculators.emt import EMT
from deepmd.calculator import DP
from ase.io import write
from ase import units
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.npt import NPT
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution,Stationary
from ase.io import write,Trajectory
from ase.md import MDLogger
from ase.geometry.analysis import Analysis
from ase.build import molecule

#choose label
label=1
## choose prefix
# prefix="tutorial"
prefix="openmx"

# atoms = molecule('CH4')
## take care of "positions"　#Ang 1e-10
atoms=Atoms(
      "CH4",
      positions=[
        ( 0.000000,    0.000000,    0.000000),
        (-0.889981,   -0.629312,    0.000000),
        ( 0.000000,    0.629312,   -0.889981),
        ( 0.000000,    0.629312,    0.889981),
        ( 0.889981,   -0.629312,    0.000000)
      ],  
      cell=[10, 10, 10],
)

write(f"img/{prefix}.png", atoms, rotation="30x, 30y, 30z")

## choose model
# atoms.set_calculator(EMT())
atoms.set_calculator(DP(model=f"{label}1.train/graph.pb"))

dt = 1.0 * units.fs

## choose temps, steps
temp0, nsteps0 = 200, 200
temp1, nsteps1 = 300, 600
taut = 1.0 * units.fs #used in NVTB
num_interval=10

MaxwellBoltzmannDistribution(atoms, temp0*units.kB)

## choose a method
dyn = NVTBerendsen(atoms, dt, temp0, taut=taut, trajectory=f'traj/{prefix}.traj')

def calculate_angle(v1, v2):
    # ベクトルv1とv2の内積を計算
    dot_product = np.dot(v1, v2)
    
    # ベクトルv1とv2のノルムを計算
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    # アークコサインを使用して角度を計算
    angle_rad = np.arccos(dot_product / (norm_v1 * norm_v2))
    
    # ラジアンから度に変換
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg

print("# time[fs] length[A] length[A] length[A] length[A] angle[deg] angle[deg] angle[deg]")
# print(atoms.symbols[0])
# print(atoms.symbols[1]) 
# print(atoms.symbols[2])
# print(atoms.symbols[3])
def myprint():
    global l_mean,ang_mean
    vec1=atoms.positions[0]-atoms.positions[1]
    vec2=atoms.positions[0]-atoms.positions[2]
    vec3=atoms.positions[0]-atoms.positions[3]

    # print(f'time={dyn.get_time() / units.fs: 5.0f} fs '+f'T={atoms.get_temperature(): 3.0f} K ')
    print(f'{ dyn.get_time()/units.fs:5.0f}   '+f'{np.linalg.norm(vec1):5.3f}   '+f'{np.linalg.norm(vec2):5.3f}   '+f'{np.linalg.norm(vec3):5.3f}   '+f'{calculate_angle(vec1,vec2):5.3f}   '+f'{calculate_angle(vec2,vec3):5.3f}   '+f'{calculate_angle(vec3,vec1):5.3f}')

dyn.attach(myprint, interval=10)
dyn.attach(MDLogger(dyn, atoms, f"log/{prefix}.log", header=True, peratom=True, mode="w"), interval=num_interval)

dyn.run(nsteps0)
dyn.set_temperature(temp1)
dyn.run(nsteps1)

traj=Trajectory(f"traj/{prefix}.traj")
# write(f"gif/{prefix}.gif", traj[::10], rotation="30x,30y,30z")