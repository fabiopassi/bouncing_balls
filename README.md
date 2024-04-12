# bouncing_balls

## Physics background

Simulation of bouncing balls. The rules are the following:

* The only force acting on the particles is gravity
* Each particle undergoes elastic collisions with the other particles and the walls

## Technical details

The scripts are written in python. The only additional packages required to run the simulation are `numpy`, `numba` and `matplotlib`; if you have conda installed, the command:

```bash
conda create -n bouncing_balls numba matplotlib
```

should create an environment with all the necessary packages.

After this, you can start the simulations with the commands:

```bash
conda activate bouncing_balls
python main.py
```
