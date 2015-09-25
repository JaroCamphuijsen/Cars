

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:27:37 2015

@author: Jaromir Camphuijsen (6042473) and Eva van Weel(10244743)
"""

#This code is based on code found at: http://www.vtk.org/gitweb?p=VTK.git;
#a=blob;f=Examples/Medical/Python/Medical3.py

import Tkinter
import vtk
from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget

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
contour.SetPosition(400, 200, 400)
contour.SetOrientation(270, 0, 180)
contour.SetMapper(dataMapper)

#length = reader.GetOutput().GetLength()

#maxVelocity =reader.GetOutput().GetPointData().GetVectors().GetMaxNorm()
#maxTime = 35.0*length/maxVelocity

#==============================================================================
# # Now we will generate a single streamline in the data. We select the
# # integration order to use (RungeKutta order 4) and associate it with
# # the streamer. The start position is the position in world space
# # where we want to begin streamline integration; and we integrate in
# # both directions. The step length is the length of the line segments
# # that make up the streamline (i.e., related to display). The
# # IntegrationStepLength specifies the integration step length as a
# # fraction of the cell size that the streamline is in.
# integ = vtk.vtkRungeKutta4()
# streamer = vtk.vtkStreamTracer()
# streamer = vtk.vtkStreamTracer()
# streamer.SetInputConnection(reader.GetOutputPort())
# streamer.SetStartPosition(0.1,2.1,0.5)
# streamer.SetMaximumPropagation(500)
# streamer.SetIntegrationStepUnit(2)
# streamer.SetMinimumIntegrationStep(0.1)
# streamer.SetMaximumIntegrationStep(1.0)
# streamer.SetInitialIntegrationStep(0.2)
# streamer.SetIntegrationDirection(0)
# streamer.SetIntegrator(integ)
# streamer.SetRotationScale(0.5)
# streamer.SetMaximumError(1.0e-8)
# 
# # The tube is wrapped around the generated streamline. By varying the
# # radius by the inverse of vector magnitude, we are creating a tube
# # whose radius is proportional to mass flux (in incompressible flow).
# streamTube = vtk.vtkTubeFilter()
# streamTube.SetInputConnection(streamer.GetOutputPort())
# streamTube.SetRadius(0.02)
# streamTube.SetNumberOfSides(12)
# streamTube.SetVaryRadiusToVaryRadiusByVector()
# 
# mapStreamTube = vtk.vtkPolyDataMapper()
# mapStreamTube.SetInputConnection(streamTube.GetOutputPort())
# mapStreamTube.SetScalarRange(reader.GetOutput().GetPointData().GetScalars().GetRange())
# 
# streamTubeActor = vtk.vtkActor()
# streamTubeActor.SetMapper(mapStreamTube)
#==============================================================================
#streamTubeActor.GetProperty().BackfaceCullingOn()





#Create outline to show extent of the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetPosition(400, 200, 400)
outline.SetOrientation(270, 0, 180)
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

#Add actors to the renderer
aRenderer.AddActor(outline)
aRenderer.AddActor(contour)

# Camera (viewpoint) settings
aCamera = vtk.vtkCamera()
aRenderer.SetActiveCamera(aCamera)
aCamera.SetPosition(0,0,-1)
aCamera.Azimuth(-45)
aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
# be displayed on starting the visualization
aCamera.Dolly(1.3)



root.mainloop()



