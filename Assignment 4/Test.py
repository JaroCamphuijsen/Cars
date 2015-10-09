# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 13:54:04 2015

@author: Eva van Weel
"""

#!/usr/bin/env python
import Tkinter, random
import vtk
from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget

root = Tkinter.Tk() 
aRenderer = vtk.vtkRenderer()
aRenderer.TexturedBackgroundOn()
renderWidget = vtkTkRenderWidget(root,width=800,height=600)
renderWidget.pack(expand='true',fill='both')
renWin = renderWidget.GetRenderWindow()
renWin.AddRenderer(aRenderer)
aRenderer.SetBackground(1, 1, 1)
renWin.SetSize(600, 480)


reader = vtk.vtkImageReader()
#reader.ReleaseDataFlagOff()
#reader.SetDataByteOrderToLittleEndian()
#reader.SetDataMask(0x7fff)
reader.SetDataExtent(0, 499, 0, 469, 1, 136)
reader.SetDataScalarTypeToUnsignedChar()
reader.SetFilePrefix("./WholeFrog/frog.")
reader.SetFilePattern("%s%03d.raw")
reader.SetDataSpacing(1,1,1.5)


# Create transfer functions for opacity and color
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20,0.0)
opacityTransferFunction.AddPoint(255,1.0)
colorTransferFunction = vtk.vtkColorTransferFunction()
# Improve coverage
colorTransferFunction.SetColorSpaceToRGB()
colorTransferFunction.AddRGBPoint(1,0,0,1)
#colorTransferFunction.RemovePoint(200)
#colorTransferFunction.AddHSVPoint(100,1,1,1)
#colorTransferFunction.AddRGBSegment(60,1,1,1,90,0,0,0)
#colorTransferFunction.AddHSVSegment(90,1,1,1,105,0,0,0)
#colorTransferFunction.RemoveAllPoints()
colorTransferFunction.SetColorSpaceToHSV()
# Create properties, mappers, volume actors, and ray cast function
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.SetInterpolationTypeToLinear()
compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())
volumeMapper.SetVolumeRayCastFunction(compositeFunction)
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
## Create geometric sphere
#sphereSource = vtk.vtkSphereSource()
#sphereSource.SetCenter(25,25,25)
#sphereSource.SetRadius(30)
#sphereSource.SetThetaResolution(15)
#sphereSource.SetPhiResolution(15)
#sphereMapper = vtk.vtkPolyDataMapper()
#sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
#sphereActor = vtk.vtkActor()
#sphereActor.SetMapper(sphereMapper)
# Set up the planes
#plane1 = vtk.vtkPlane()
#plane1.SetOrigin(25,25,20)
#plane1.SetNormal(0,0,1)
#plane2 = vtk.vtkPlane()
#plane2.SetOrigin(25,25,30)
#plane2.SetNormal(0,0,-1)
#plane3 = vtk.vtkPlane()
#plane3.SetOrigin(20,25,25)
#plane3.SetNormal(1,0,0)
#plane4 = vtk.vtkPlane()
#plane4.SetOrigin(30,25,25)
#plane4.SetNormal(-1,0,0)
#sphereMapper.AddClippingPlane(plane1)
#sphereMapper.AddClippingPlane(plane2)
#volumeMapper.AddClippingPlane(plane3)
#volumeMapper.AddClippingPlane(plane4)
## Okay now the graphics stuff
#aRenderer.AddActor(sphereActor)
aRenderer.AddVolume(volume)

aCamera = vtk.vtkCamera()
aRenderer.SetActiveCamera(aCamera)
aCamera.SetPosition(0,0,-1)
aCamera.Azimuth(-45)
aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
# be displayed on starting the visualization
aCamera.Dolly(1.3)
root.mainloop()
# --- end of script --