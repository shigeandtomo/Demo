from ase.build import bulk

def calc_density_energy(symbol: str = "Fe", crystalstructure: str = "bcc"):
    a_array = np.linspace(2.0, 8.0, 30)

    energy_list = []
    density_list = []
    for a in a_array:
        # atoms = bulk(symbol, crystalstructure, a=a)
        atoms = bulk(name="C", crystalstructure="diamond", a=a).repeat((2,2,2))
        # atoms.calc = calculator
        label=1
        atoms.set_calculator(DP(model=f"{label}1.train/graph.pb"))
        E_pot = atoms.get_potential_energy() / len(atoms)
        density = len(atoms) / atoms.get_volume()
        energy_list.append(E_pot)
        density_list.append(density)
    return np.array(energy_list), np.array(density_list)

diamond_energy, diamond_density = calc_density_energy("C", "diamond")