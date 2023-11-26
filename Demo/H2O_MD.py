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

## choose label
label=2
## choose prefix
# prefix="emt"
# prefix="dp_vasp"
prefix="H2O"
# prefix="dp_abcus"

## take care of "positions"
atoms=Atoms(
      "H2O",
      positions=[
      ( 0.757,  0.586,  0.000),
      (-0.757,  0.586,  0.000),
      ( 0.000,  0.000,  0.000)
      ],
      cell=[10, 10, 10],
)

write(f"img/{prefix}.png", atoms, rotation="30x, 30y, 30z")

## choose model
# atoms.set_calculator(EMT())
atoms.set_calculator(DP(model=f"{label}1.train/graph.pb"))

dt = 1.0 * units.fs

## choose temps, steps
temp0, nsteps0 = 300, 200
temp1, nsteps1 = 300, 600
taut = 1.0 * units.fs #used in NVTB
# ttime= 40.0*units.fs #used in N-H
num_interval=10

MaxwellBoltzmannDistribution(atoms, temp0*units.kB)
# MaxwellBoltzmannDistribution(atoms, temperature_K=temp0,force_temp=True)
# Stationary(atoms)

## choose a method
dyn = NVTBerendsen(atoms, dt, temp0, taut=taut, trajectory=f'traj/{prefix}.traj')
# dyn = NPT(atoms,dt,
#           temperature_K=temp0,
#           externalstress = 0.1e-6 * units.GPa,  # Ignored in NVT
#           ttime = ttime,
#           pfactor = None,   # None for NVT
#           trajectory=f'traj/{prefix}.traj'
          # )

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

print("# time[fs] length[A] length[A] angle[deg]")
def myprint():
    vec1=atoms.positions[0]-atoms.positions[2]
    vec2=atoms.positions[1]-atoms.positions[2]

    # print(f'time={dyn.get_time() / units.fs: 5.0f} fs '+f'T={atoms.get_temperature(): 3.0f} K ')
    print(f'{ dyn.get_time()/units.fs:5.0f}   '+f'{np.linalg.norm(vec1):5.3f}   '+f'{np.linalg.norm(vec2):5.3f}   '+f'{calculate_angle(vec1,vec2):5.3f}')

dyn.attach(myprint, interval=10)
dyn.attach(MDLogger(dyn, atoms, f"log/{prefix}.log", header=True, peratom=True, mode="w"), interval=num_interval)

dyn.run(nsteps0)
dyn.set_temperature(temp1)
dyn.run(nsteps1)

traj=Trajectory(f"traj/{prefix}.traj")
## make gif file
# write(f"gif/{prefix}.gif", traj[::10], rotation="30x,30y,30z")

### ステップ毎のRDFをgifに保存　###
# from ase.geometry.analysis import Analysis
# import matplotlib.pyplot as plt

# for idx in range(801):
#       plt.xlabel("r [angst]")
#       plt.ylabel("rho(r)")
#       plt.xlim(0.0,5.0)
#       plt.ylim(0,100)
#       distribution, distance = Analysis(traj[idx]).get_rdf(rmax=5., nbins=100, return_dists=True)[0]
#       plt.plot(distance, distribution, color='darkblue')
#       plt.savefig(f"frames/frame{idx}.png")
#       plt.clf()
      
# from PIL import Image
# import glob

# # 画像ファイルのパスを取得
# image_files = sorted(glob.glob('frames/frame*.png'))  # 連番のファイル名に合わせてパターンを指定

# # # GIFを保存するためのリスト
# images = []

# # # 画像をGIFに追加
# for image_file in image_files:
#     img = Image.open(image_file)
#     images.append(img)

# # GIFを保存
# images[0].save('output.gif', save_all=True, append_images=images[1:], duration=300, loop=0) #duration[ms]