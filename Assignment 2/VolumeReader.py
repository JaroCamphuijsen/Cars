# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:27:37 2015

@author: Eva van Weel
"""

#!/usr/bin/env python

# This example reads a volume dataset, extracts an isosurface that
# represents the skin and displays it.

import sys
import Tkinter
import vtk
from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget



# Create the renderer, the render window, and the interactor. The
# renderer draws into the render window, the interactor enables mouse-
# and keyboard-based interaction with the scene.
aRenderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(aRenderer)
iren = vtk.vtkRenderWindowInteractor()
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.SetRenderWindow(renWin)

# The following reader is used to read a series of 2D slices (images)
# that compose the volume. The slice dimensions are set, and the
# pixel spacing. The data Endianness must also be specified. The reader
# usese the FilePrefix in combination with the slice number to construct
# filenames using the format FilePrefix.%d. (In this case the FilePrefix
# is the root name of the file: quarter.)
v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(256, 256)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(".\Data\slice")
v16.SetImageRange(1, 94)


spacing = v16.GetOutput().GetSpacing()
sx, sy, sz = spacing
v16.SetDataSpacing(sx, sy, sz)

#print sz

im = v16.GetImage(6)

# histogram = vtk.vtkImageAccumulate()
# histogram.SetInputConnection(im.GetOutputPort())
# histogram.SetComponentExtent(0,255,0,0,0,0)
# histogram.SetComponentOrigin(0,0,0)
# histogram.SetComponentSpacing(1,0,0)
# histogram.IgnoreZeroOn()
# histogram.Update()

# An isosurface, or contour value of 500 is known to correspond to the
# skin of the patient. Once generated, a vtkPolyDataNormals filter is
# is used to create normals for smooth surface shading during rendering.
# The triangle stripper is used to create triangle strips from the
# isosurface these render much faster on may systems.
skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(v16.GetOutputPort())
<<<<<<< HEAD
skinExtractor.SetValue(0, 2800)
=======
skinExtractor.SetValue(0, 300)
>>>>>>> 876e82b4c9d09ad492a9d077eb4af7d5b3d0adac
skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(20.0)
skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper.ScalarVisibilityOff()
skin = vtk.vtkActor()
skin.SetMapper(skinMapper)



# It is convenient to create an initial view of the data. The FocalPoint
# and Position form a vector direction. Later on (ResetCamera() method)
# this vector is used to position the camera to look at the data in
# this direction.
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

# Actors are added to the renderer. An initial camera view is created.
# The Dolly() method moves the camera towards the FocalPoint,
# thereby enlarging the image.
aRenderer.AddActor(skin)
aRenderer.SetActiveCamera(aCamera)
aRenderer.ResetCamera()
aCamera.Dolly(1.5)

# Set a background color for the renderer and set the size of the
# render window (expressed in pixels).
aRenderer.SetBackground(1, 1, 1)
renWin.SetSize(640, 480)

class scale:
    "Scale"
    def __init__(self, root, renWin, sphere):
        self.renWin, self.sphere = renWin, sphere
        scale = Tkinter.Scale(root, from_=0, to=3000,resolution=1.0, orient= "horizontal", command=self.change)
        scale.pack(side='bottom')

    def change(self, val):
        # This strange int(float()) conversion is required....
        skinExtractor.SetValue(0, int(float(val)))
        self.renWin.Render()


root = Tkinter.Tk() 

renderWidget = vtkTkRenderWidget(root,width=400,height=400)
renderWidget.pack(expand='true',fill='both')

renWin = renderWidget.GetRenderWindow()

ren = vtk.vtkRenderer()
renWin.AddRenderer(aRenderer)
ren.AddActor(skin)

scale=scale(root, renWin, skinExtractor)







# Interact with the data.
#iren.Initialize()
#renWin.Render()
#iren.Start()
root.mainloop()


