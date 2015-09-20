# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:27:37 2015

@author: Jaromir Camphuijsen (6042473) and Eva van Weel(10244743)
"""

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
v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(256, 256)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(".\Data\slice") #Loop through all slices
v16.SetImageRange(1, 94) #Number of images to loop through

#Slice spacing
spacing = lambda: [3.2, 3.2, 5]
sx, sy, sz = spacing()
v16.SetDataSpacing(sx, sy, sz)
v16.Update()
#Read the scalar value range
scalarMin, scalarMax = v16.GetOutput().GetScalarRange()


#Create an isosurface and use vtkPolyDataNormals to create normals for smooth 
#surface shading.The triangle stripper is used to create triangle strips from 
#the isosurface which render much faster on many systems.
skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(v16.GetOutputPort())
skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)
skinStripper = vtk.vtkStripper()
skinStripper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinStripper.GetOutputPort())
skinMapper.ScalarVisibilityOff()
skin = vtk.vtkActor()
skin.SetMapper(skinMapper)

#Create outline to show extent of the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(v16.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

#Add actors to the renderer
aRenderer.AddActor(outline)
aRenderer.AddActor(skin)

# Camera (viewpoint) settings
aCamera = vtk.vtkCamera()
aCamera.SetPosition(0,0, -4000)
aCamera.ComputeViewPlaneNormal()
aRenderer.SetActiveCamera(aCamera)
aRenderer.ResetCamera()
aCamera.Dolly(1.5) #Move camera to vocal point

#Class which allows the interactivity of the slider. Based on code from:
#http://www.uppmax.uu.se/docs/w/index.php/TkInter
class scale:
    "Scale"
    def __init__(self, root, renWin, skinExtractor):
        self.renWin, self.skinExtractor = renWin, skinExtractor
        scale = Tkinter.Scale(root, length=1000, from_=scalarMin, to=scalarMax,resolution=.1, orient= "horizontal", command=self.change)
        scale.set(scalarMax/2)  
        scale.pack(side='bottom')

    def change(self, val):
        skinExtractor.SetValue(0, int(float(val)))
        self.renWin.Render()


scale=scale(root, renWin, skinExtractor)
root.mainloop()


