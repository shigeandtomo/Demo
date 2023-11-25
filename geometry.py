#!/usr/bin/python3
### This file is made for checking bond length and angles ###

import os, sys
import numpy as np
from collections import OrderedDict

length_convert=1.0
energy_convert=1.0
force_convert=1.0

def load_param_file(fname):
    # atom_names=load_atom(fname, "Atoms.SpeciesAndCoordinates")
    # cell=load_cell(fname, "Atoms.UnitVectors")
    with open(fname, "r") as dat_file:
        lines = dat_file.readlines()
        atom_names, cell = [], []
        atom_names_mode, cell_mode = False, False
        for line in lines:
            if "<Atoms.SpeciesAndCoordinates" in line:
                atom_names_mode = True
            elif "Atoms.SpeciesAndCoordinates>" in line:
                atom_names_mode = False
            elif atom_names_mode:
                parts = line.split()
                atom_names.append(parts[1])
            elif "<Atoms.UnitVectors" in line:
                cell_mode = True
            elif "Atoms.UnitVectors>" in line:
                cell_mode = False
            elif cell_mode:
                parts = line.split()
                cell.append(parts)
        # print(atom_names)
        natoms=len(atom_names)
        atom_names = list(OrderedDict.fromkeys(set(atom_names))) #注: Python3.7以降
        # atom_names = list(set(atom_names)) #注: Python3.7以前
        ntypes=len(atom_names)
        # cell=np.array(cell).astype(float)
        cell=np.array([[10,0,0],[0,10,0],[0,0,10]])
        atom_numbs = [0] * ntypes
        atom_types = []
        coords_mode = False
        for line in lines:
            if "<Atoms.SpeciesAndCoordinates" in line:
                coords_mode = True
            elif "Atoms.SpeciesAndCoordinates>" in line:
                coords_mode = False
            elif coords_mode:
                parts = line.split()
                for i, atom_name in enumerate(atom_names):
                    if parts[1] == atom_name:
                        atom_numbs[i]+=1
                        atom_types.append(i)
        if natoms != len(atom_types):
            raise ValueError("Input file is incorrect.")
        else:
            atom_types = np.array(atom_types)
        ## checking output ##
        # atom_names=symbols
        # atom_numbs=[4,1]
        # atom_types=np.array([1,0,0,0,0])
        # cell=10*np.eye(3)
    return atom_names, atom_numbs, atom_types, cell

def load_data(mdname, atom_names, natoms, begin=0, step=1, convert=1.0):
    with open(mdname, "r") as md_file:
        lines = md_file.readlines()
        cnt = 0
        coord, coords=[], []
        for index, line in enumerate(lines):
            # wanna change
            if "time" in line:
                continue
            ## depend on atom_numbs ##
            for atom_name in atom_names:
                atom_name+=" "
                if atom_name in line:
                # elif f"{atom_names[0]} " in line or f"{atom_names[1]} " in line:
                # elif f"{atom_names[0]} " in line:
                    cnt+=1
                    parts = line.split()
                    for_line = [float(parts[1]),float(parts[2]),float(parts[3])]
                    coord.append(for_line)
            if cnt==natoms:
                coords.append(coord)
                cnt=0
                coord=[]
        coords=np.array(coords)
        steps=[str(i) for i in range(1, coords.shape[0]+1)]
        ## checking output ##
        # coords = np.random.rand(200,5,3)
        # steps = [str(i) for i in range(1, coords.shape[0]+1)]
    return coords, steps

def to_system_data(fname, mdname, begin=0, step=1):
    data = {}
    data["atom_names"], data["atom_numbs"], data["atom_types"], cell = load_param_file(fname)
    data["coords"], csteps = load_data(
        mdname,
        data["atom_names"],
        np.sum(data["atom_numbs"]),
        begin=begin,
        step=step,
        convert=length_convert,
    )
    data["orig"] = np.zeros(3)
    data["cells"]= np.array([cell for _ in range(len(csteps))])
    return data, csteps

def to_system_label(fname, mdname, data, begin=0, step=1):
    atom_names, atom_numbs, atom_types, cell = load_param_file(fname)
    with open(mdname, "r") as md_file:
        lines = md_file.readlines()
        cnt=0
        energy = []
        field, fields = [], []
        for index, line in enumerate(lines):
            if "time" in line:
                parts = line.split()
                evp_line = float(parts[4])  # Hartree
                energy.append(evp_line)
                continue
            ## depend on atom_numbs ##
            for atom_name in atom_names:
                atom_name+=" "
                if atom_name in line:
                    # elif data["atom_names"][0]+" " in line or data["atom_names"][1]+" " in line:
                    # elif data["atom_names"][0]+" " in line:
                    cnt += 1
                    parts = line.split()
                    for_line = [float(parts[4]),float(parts[5]),float(parts[6])]
                    field.append(for_line)
            if cnt==np.sum(data["atom_numbs"]):
                fields.append(field)
                cnt = 0
                field = []
        energy=energy_convert*np.array(energy) #Hartree->eV
        force=force_convert*np.array(fields)
        ## checking output ##
        # energy=np.array([-29933]*200)
        # force=np.random.rand(200,5,3)
        # esteps=[str(i) for i in range(1, 201)]
    return energy, force

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

if __name__ == "__main__":
    label=2
    omx_input_name = "H2O"
    System_name = "H2O"
    fname=f"{label}0.data/{omx_input_name}.dat"
    mdname=f"{label}0.data/{System_name}.md"
    atom_names, atom_numbs, atom_types, cell = load_param_file(fname)
    coords, steps = load_data(mdname, atom_names, np.sum(atom_numbs))
    # cells, _ = load_data(prefix + ".cel", 3)
    data, csteps=to_system_data(
        fname, mdname, begin=0, step=1
    )
    energy, force=to_system_label(
        fname, mdname, data, begin=0, step=1
    )
    # print(atom_names)
    # print(atom_numbs)
    # print(atom_types)
    # print(cell)
    # print(cell.shape)
    # print(coords.shape)
    # print(coords)
    # print(data["coords"].shape)
    # print(csteps)
    # print(energy)
    # print(len(energy))
    # print(force)
    # print(force.shape)

    cnt=0
    # print("# time[fs] length[Å] length[Å] length[Å] length[Å] angle[deg] angle[deg] angle[deg]")
    print("# time[fs] length[Å] length[Å] angle[deg]")
    for coord in coords:
        vec1=coord[0]-coord[1]
        vec2=coord[0]-coord[2]
        # vec3=coord[0]-coord[3]
        # print(f'{cnt:2.0f}   '+f'{np.linalg.norm(vec1):5.3f}   '+f'{np.linalg.norm(vec2):5.3f}   '+f'{np.linalg.norm(vec3):5.3f}   '+f'{calculate_angle(vec1,vec2):5.3f}   '+f'{calculate_angle(vec2,vec3):5.3f}   '+f'{calculate_angle(vec3,vec1):5.3f}')
        print(f'{cnt:2.0f}   '+f'{np.linalg.norm(vec1):5.3f}   '+f'{np.linalg.norm(vec2):5.3f}   '+f'{calculate_angle(vec1,vec2):5.3f}   ')
        cnt+=1
        