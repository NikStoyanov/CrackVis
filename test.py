"""
Test case to plot the principal stress
and the temperature
"""

from plot_3d import VtkPointCloud, SetVtkWindow

filename = "/home/nik/Dropbox/PhD/Academic/Modelling/Abaqus/Crack_Vis/output_data/2D_Crack_Vis_m160C_200MPa/2D_Crack_Vis_m160C_200MPa.dat"

# display the principal stress
point_cloud = VtkPointCloud(filename, 10**8, 7, 10)
point_cloud.load_data()
vtk_window = SetVtkWindow(point_cloud)

# display the temperature
point_cloud = VtkPointCloud(filename, 10**2, 3, 10)
point_cloud.load_data()
vtk_window = SetVtkWindow(point_cloud)