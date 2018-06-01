import sys
import vtk
import numpy as np

class VtkPointCloud:
    """
    Makes the point cloud
    """
    def __init__(self):
        """
        Setup init functions for the vtk point cloud
        """

        self.vtkPolyData = vtk.vtkPolyData()
        self.clear_points()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputData(self.vtkPolyData)
        self.mapper.SetColorModeToDefault()
        self.mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.mapper)
        self.vtkActor.GetProperty().SetPointSize(5)

        self.mesh_actor = vtk.vtkActor()
        self.scalar_bar_actor = vtk.vtkScalarBarActor()
        self.mesh_mapper = vtk.vtkDataSetMapper()

    def add_point(self, point):
        """
        Adds a point to the point cloud

        Args:
            point (float): array holding x,y,z
        """

        pointId = self.vtkPoints.InsertNextPoint(point[0], point[1], point[2])
        self.vtkDepth.InsertNextValue(point[2])
        self.vtkCells.InsertNextCell(1)
        self.vtkCells.InsertCellPoint(pointId)

        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def set_range(self, min_data, max_data):
        """
        Sets the scalar range

        Args:
            min_data (float): the minimum value in z
            max_data (float): the maximum value in z
        """

        self.mapper.SetScalarRange(min_data, max_data)

    def clear_points(self):
        """
        Clears the points
        """

        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

class SetVtkWindow():
    """
    Sets the window interactions
    """
    def __init__(self, point_cloud):
        # set renderer
        renderer = vtk.vtkRenderer()
        renderer.AddActor(point_cloud.vtkActor)
        renderer.SetBackground(0., 0., 0.)
        renderer.ResetCamera()

        # set the window
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)

        # set interactor
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # start interactor
        renderWindow.Render()
        renderWindow.SetWindowName("CrackVis:" + filename)
        renderWindowInteractor.Start()

    def draw_color_range(self, mesh_lookup_table):
        """
        Draw the scalar range so that red is max, blue is min
        """

        self.mesh_lookup_table = vtk.vtkLookupTable()
        self.draw_color_range(self.mesh_lookup_table)
        self.mesh_lookup_table.Build()

        self.mesh_mapper.SetScalarRange(min_data, max_data)
        self.mesh_mapper.SetLookupTable(self.mesh_lookup_table)

        self.scalar_bar_actor.SetOrientationToVertical()
        self.scalar_bar_actor.SetLookupTable(self.mesh_lookup_table)

        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(renderWindowInteractor)
        scalar_bar_widget.SetScalarBarActor(self.scalar_bar_actor)

        self.mesh_lookup_table.SetHueRange(0.667, 0)

def load_data(filename, point_cloud):
    """
    Load a csv dataset which consists of exported ABAQUS data

    Args:
        point_cloud (VtkPointCloud): point cloud object
    """

    data = np.genfromtxt(filename, dtype=float, usecols=[1, 2, 7], delimiter=' ')

    # scale the data so it can be displayed properly
    data[:, 2] = data[:, 2] / (10**8)

    # identify extremums to set the scalar range
    min_data = np.min(data[:, 2])
    max_data = np.max(data[:, 2])

    point_cloud.set_range(min_data, max_data)

    # add the points
    for point_counter in range(data.shape[0]):
        point = data[point_counter]
        point_cloud.add_point(point)

    return point_cloud

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = input("Enter file name: ")

    filename = "/home/nik/Dropbox/PhD/Academic/Modelling/Abaqus/Crack_Vis/output_data/2D_Crack_Vis_m160C_200MPa/2D_Crack_Vis_m160C_200MPa.dat"
    point_cloud = VtkPointCloud()
    point_cloud = load_data(filename, point_cloud)

    vtk_window = SetVtkWindow(point_cloud)
