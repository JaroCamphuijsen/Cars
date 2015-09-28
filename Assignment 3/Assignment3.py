

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:27:37 2015

@author: Jaromir Camphuijsen (6042473) and Eva van Weel(10244743)
"""

#This code is based on code found at: http://www.vtk.org/gitweb?p=VTK.git;
#a=blob;f=Examples/Medical/Python/Medical3.py

import Tkinter, random
import vtk
from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget
nPoints = 300
# Create the renderer and the GUI
root = Tkinter.Tk() 
aRenderer = vtk.vtkRenderer()
aRenderer.TexturedBackgroundOn()
renderWidget = vtkTkRenderWidget(root,width=800,height=600)
renderWidget.pack(expand='true',fill='both')
renWin = renderWidget.GetRenderWindow()
renWin.AddRenderer(aRenderer)
aRenderer.SetBackground(1, 1, 1)
renWin.SetSize(600, 480)

# Read the 2D images (CT scan slices). 
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("./SMRX.vtk")

scalarMin, scalarMax = reader.GetOutput().GetScalarRange()


#Create an isosurface and use vtkPolyDataNormals to create normals for smooth 
#surface shading.
contourFilter = vtk.vtkContourFilter()
contourFilter.SetInputConnection(reader.GetOutputPort())
contourFilter.SetValue(0,1)
contourNormals = vtk.vtkPolyDataNormals()
contourNormals.SetInputConnection(contourFilter.GetOutputPort())
contourNormals.SetFeatureAngle(60.0)
dataMapper = vtk.vtkPolyDataMapper()
dataMapper.SetInputConnection(contourNormals.GetOutputPort())
dataMapper.ScalarVisibilityOff() 
contour = vtk.vtkActor()
contour.SetMapper(dataMapper)
contour.GetProperty().SetOpacity(0.25)


pointSource1 = vtk.vtkProgrammableSource()
pointSource2 = vtk.vtkProgrammableSource()

def points1():
    output = pointSource1.GetPolyDataOutput()
    points1 = vtk.vtkPoints()
    output.SetPoints(points1)

    for i in range(nPoints):
        x, y, z = 1.5, (.5 + random.randint(0,30)), (.5 + random.randint(0,60))
        points1.InsertNextPoint(x, y, z)

def points2():
    output = pointSource2.GetPolyDataOutput()
    points2 = vtk.vtkPoints()
    output.SetPoints(points2)

    for i in range(nPoints):
        x, y, z = 1.5, (.5 + random.randint(30,60)), (.5 + random.randint(0,60))
        points2.InsertNextPoint(x, y, z)

pointSource1.SetExecuteMethod(points1)
pointSource2.SetExecuteMethod(points2)

integ = vtk.vtkRungeKutta45()
streamer1 = vtk.vtkStreamTracer()
streamer1.SetInputConnection(reader.GetOutputPort())
streamer1.SetSourceConnection(pointSource1.GetOutputPort())
streamer1.SetMaximumPropagation(2000) 
streamer1.SetIntegrationStepUnit(2) #Cell length unit
streamer1.SetMinimumIntegrationStep(0.01)
streamer1.SetMaximumIntegrationStep(10)
streamer1.SetInitialIntegrationStep(0.2)
streamer1.SetIntegrationDirection(0)
streamer1.SetIntegrator(integ)
streamer1.SetRotationScale(0.5)

streamer2 = vtk.vtkStreamTracer()
streamer2.SetInputConnection(reader.GetOutputPort())
streamer2.SetSourceConnection(pointSource2.GetOutputPort())
streamer2.SetMaximumPropagation(2000) 
streamer2.SetIntegrationStepUnit(2) #Cell length unit
streamer2.SetMinimumIntegrationStep(0.01)
streamer2.SetMaximumIntegrationStep(10)
streamer2.SetInitialIntegrationStep(0.2)
streamer2.SetIntegrationDirection(0)
streamer2.SetIntegrator(integ)
streamer2.SetRotationScale(0.5)

streamTube1 = vtk.vtkTubeFilter()
streamTube1.SetInputConnection(streamer1.GetOutputPort())
streamTube1.SetRadius(.25)
streamTube1.SetNumberOfSides(12)
streamTube1.SetCapping(1)


streamTube2 = vtk.vtkTubeFilter()
streamTube2.SetInputConnection(streamer2.GetOutputPort())
streamTube2.SetRadius(.25)
streamTube2.SetNumberOfSides(12)
streamTube2.SetCapping(1)


vLookupTable = vtk.vtkLookupTable()
vLookupTable.SetValueRange(0.5,1)

mapStreamTube1 = vtk.vtkPolyDataMapper()
mapStreamTube1.SetInputConnection(streamTube1.GetOutputPort())
mapStreamTube1.SetLookupTable(vLookupTable)
mapStreamTube1.SetScalarVisibility(0)	



mapStreamTube2 = vtk.vtkPolyDataMapper()
mapStreamTube2.SetInputConnection(streamTube2.GetOutputPort())
mapStreamTube2.SetLookupTable(vLookupTable)
mapStreamTube2.SetScalarVisibility(0)



streamTubeActor1 = vtk.vtkActor()
streamTubeActor1.SetMapper(mapStreamTube1)
streamTubeActor1.GetProperty().BackfaceCullingOn()
streamTubeActor1.GetProperty().SetColor(1, 0, 0)


streamTubeActor2 = vtk.vtkActor()
streamTubeActor2.SetMapper(mapStreamTube2)
streamTubeActor2.GetProperty().BackfaceCullingOn()
streamTubeActor2.GetProperty().SetColor(0,1,0)

#Create outline to show extent of the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

# Create a vtkLight, and set the light parameters.
light = vtk.vtkLight()
light.SetFocalPoint(0, 0, 0)
light.SetPosition(0, 200, 0)

#Add actors to the renderer
aRenderer.AddActor(outline)
aRenderer.AddActor(streamTubeActor1)
aRenderer.AddActor(streamTubeActor2)
aRenderer.AddActor(contour)
aRenderer.AddLight(light)

# Camera (viewpoint) settings
aCamera = vtk.vtkCamera()
aRenderer.SetActiveCamera(aCamera)
aCamera.SetPosition(0,0,-1)
aCamera.Azimuth(-45)
aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
# be displayed on starting the visualization
aCamera.Dolly(1.3)



root.mainloop()



