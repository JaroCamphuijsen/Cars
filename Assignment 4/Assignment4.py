

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:27:37 2015

@author: Jaromir Camphuijsen (6042473) and Eva van Weel(10244743)
"""

import Tkinter, random
import vtk
from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget

# Create the renderer and the GUI
tissueList = ["Blood", "Brain", "Duodenum", "Eye retina", 
"Eye white", "Heart", "Ileum", "Kidney", "Large intestine",
"Liver", "Lung", "Nerve", "Skeleton", "Spleen", "Stomach"]

tissueDict = {1: "Blood", 2: "Brain", 3: "Duodenum", 4: "Eye retina", 
5: "Eye white", 6: "Heart", 7:"Ileum", 8:"Kidney", 9:"Large intestine",
10:"Liver", 11:"Lung", 12:"Nerve", 13:"Skeleton", 14:"Spleen", 15:"Stomach"}

def createOpacityTransferFunction(values):
	opacityTransferFunction = vtk.vtkPiecewiseFunction()
	opacityTransferFunction.AddPoint(1.0, 0)
	for v in values:
		opacityTransferFunction.AddPoint(v - 1, 0)
		opacityTransferFunction.AddPoint(v, .2)
		opacityTransferFunction.AddPoint(v + 1, 0)
		
	opacityTransferFunction.AddPoint(17.0, 0)
	return opacityTransferFunction

class scale:
    "Scale"
    def __init__(self, renWin, opacityTransferFunction):
        self.renWin, self.opacityTransferFunction = renWin, opacityTransferFunction
        scale = Tkinter.Scale(root, length=1000, from_=0, to=16,
                              resolution=.1, orient= "horizontal", 
                              command=self.change)
        scale.set(1)  
        scale.pack(side='bottom')

    def change(self, val):
        self.opacityTransferFunction = createOpacityTransferFunction([int(float(val))])
        self.renWin.Render()

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
reader.SetDataExtent(0,499,0,469,1,136)
reader.SetDataSpacing(1,1,1.5)
reader.SetDataScalarTypeToUnsignedChar()
reader.SetFilePattern("./WholeFrog/frogTissue.%s%03d.raw")
# reader.SetDataMask(0x7fff)
reader.Update()

 # Create transfer mapping scalar value to opacity
opacityTransferFunction = createOpacityTransferFunction([1,2,7,9,13])

# Create transfer mapping scalar value to color
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(1.0, 0.75, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(2.0, 0.65, 0.65, 0.6)

colorTransferFunction.AddRGBPoint(4.0, 1.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(7.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(10.0, 0.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(13.0, 1.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(16.0, 1.0, 0.0, 1.0)

# The property describes how the data will look
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
# volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data
compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(compositeFunction)
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
aRenderer.AddVolume(volume)

# Camera (viewpoint) settings
aCamera = vtk.vtkCamera()
aRenderer.SetActiveCamera(aCamera)
aCamera.SetPosition(0,0,-1)
aCamera.Azimuth(-45)
aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
# be displayed on starting the visualization
aCamera.Dolly(1.3)

scale=scale(renWin, opacityTransferFunction)



root.mainloop()



