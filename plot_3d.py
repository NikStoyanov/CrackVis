import sys
import vtk
import numpy as np

class VtkPointCloud:
    def __init__(self):
        """
        Setup init functions for vtk
        """

        self.vtkPolyData = vtk.vtkPolyData()
        self.clear_points()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputData(self.vtkPolyData)
        self.mapper.SetColorModeToDefault()
        self.mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.mapper)

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

    def add_axis(self, limits, scale):
        self.ax3D = vtk.vtkCubeAxesActor()
        self.ax3D.ZAxisTickVisibilityOn()
        self.ax3D.SetXTitle('X')
        self.ax3D.SetXUnits('mm')
        self.ax3D.SetYTitle('Y')
        self.ax3D.SetYUnits('mm')
        self.ax3D.SetZTitle('Z')
        self.ax3D.SetZUnits('mm')
        self.ax3D.SetBounds(limits)
        self.ax3D.SetZAxisRange(limits[-2]*scale[2],limits[-1]*scale[2])
        self.ax3D.SetXAxisRange(limits[0]*scale[0],limits[1]*scale[0])
        self.ax3D.SetYAxisRange(limits[2]*scale[1],limits[3]*scale[1])
        self.ax3D.SetCamera(renderWindow.GetActiveCamera())
        renderWindow.AddActor(self.ax3D)

def load_data(filename, point_cloud):
    """
    Load a csv dataset which consists of exported ABAQUS data

    Args:
        point_cloud (VtkPointCloud): point cloud object
    """

    data = np.genfromtxt(filename, dtype=float, usecols=[1, 2, 4], delimiter=' ')

    # scale the data so it can be displayed properly
    data[:, 2] = data[:, 2] / (10**8)

    # identify extremums to set the scalar range
    min_data = np.min(data[:, 2])
    max_data = np.max(data[:, 2])

    print(min_data)
    print(max_data)

    point_cloud.set_range(min_data, max_data)

    # add the points
    for point_counter in range(data.shape[0]):
        point = data[point_counter]
        point_cloud.add_point(point)

    return point_cloud

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: xyzviewer.py itemfile")
        filename = input("Enter file name: ")

    filename = "/home/nik/Dropbox/PhD/Academic/Modelling/Abaqus/Crack_Vis/output_data/2D_Crack_Vis_m160C_200MPa/2D_Crack_Vis_m160C_200MPa.dat"
    pointCloud = VtkPointCloud()
    pointCloud = load_data(filename, pointCloud)

    # set renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor)
    #renderer.SetBackground(.2, .3, .4)
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
    renderWindow.SetWindowName("PhD Viewer:" + filename)
    renderWindowInteractor.Start()
