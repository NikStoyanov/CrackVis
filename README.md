# Background
For my PhD project I needed a tool to help me decide where to modify
my simulations (by inserting cohesive elements). This requires the
ability to see the stress state of structural elements. I am using
ABAQUS for my FE calculations, however, the visualisation side of it
is quite poor. After some digging I found [[https://sukhbinder.wordpress.com/2013/09/17/python-vtk-script-to-display-3d-xyz-data/][this article]] which details
how to do it with python and [[https://www.vtk.org/][VTK]], however, it was writing in python 2
and was missing some functionality which I need. Therefore, I made
some changes (python 3!) and added bits and pieces I needed. I also
gave it the super original name CrackVis.
#+END_abstract

CrackVis is a visualisation tool which uses [[https://www.vtk.org/][VTK]] to display a point
cloud from [[http://www.simulia.com/][ABAQUS]] 2D simulations. The input to the code is a csv file
which holds data in the following format:

| X | Y | Z1 | Z2 | ... |

Where X and Y are the coordinates of the nodes and $Z_n$ is the data
to be investigated.

The tool will plot the point cloud which represents the nodal values.

# Objective
The purpose of the script is to provide a visual perspective on the
stress distribution of structural elements which can facilitate the
seed of cohesive elements to model crack initiation and propagation.

# Parser
The parser scripts to extract data from an ABAQUS .odb file can be
found in [[https://github.com/NikStoyanov/phdfunc][this repository]].

# Usage
To use the tool you need to do import the CrackVis module, provide the file name
and set user defined properties.

The properties are:
- scaling factor: otherwise the plot will be difficult to perceive in some cases
- feature: the column of the $Z_n$ which is under investigation
- point size

# Example

Lets do an example!

A simulation with ABAQUS has been ran on a plate with the following
boundary conditions:
- U_1 = U_2 = 0 on East
- +F_1 on West
- A quadratic temperature function was applied with 0 o the boundary and -160 in the centre

The schematic is below:
[[./img/Damage_evolution_model_annon1.png]]

```python
from crackvis import VtkPointCloud, SetVtkWindow

filename = "./data/2D_Crack_Vis_m160C_200MPa.dat"

scale = 10**8
feature = 7
point_size = 10

# display the principal stress
point_cloud = VtkPointCloud(filename, scale, feature, point_size)
point_cloud.load_data()
vtk_window = SetVtkWindow(point_cloud)
```

And we get this 3D plot of the principal stress
[[./img/screen_PStress.png]]

Lets also see the temperature!

```python
scale = 10**2
feature = 3
point_size = 10

# display the temperature
point_cloud = VtkPointCloud(filename, scale, feature, point_size)
point_cloud.load_data()
vtk_window = SetVtkWindow(point_cloud)
```

Which shows the quadratic temperature function applied in the FE calculation
[[./img/screen_Temp.png]]

