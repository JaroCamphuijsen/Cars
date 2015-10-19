

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:27:37 2015

@author: Jaromir Camphuijsen (6042473) and Eva van Weel(10244743)
"""

import Tkinter, random
import vtk
from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget
from Tkinter import *

# Create the renderer and the GUI


def createOpacityTransferFunction(values):
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(1.0, 0)
    for v in values:
        opacityTransferFunction.AddPoint(v - 0.01, 0)
        opacityTransferFunction.AddPoint(v, .2)
        opacityTransferFunction.AddPoint(v + 0.01, 0)
    opacityTransferFunction.AddPoint(17.0, 0)
    return opacityTransferFunction


def visualizeTissue(v):
    allTissues = False
  
    #colorTransferFunction.AddRGBPoint(16.0, 1.0, 0.0, 1.0) #Is deze altijd nodig?
    
    #Show all tissues, not working yet :(
    if v == 0:
        if len(opacityList) == 15:
            allTissues = True
        
        for value in colourDict.iteritems():
            if allTissues:
                aRenderer.RemoveVolume(volumeDict.get(value[0]))
                opacityList.remove(value[0])
            elif value[0] not in opacityList:
                aRenderer.AddVolume(volumeDict.get(value[0]))
                
                if value[0] != 1.5:
                    opacityList.append(value[0])
    elif v == 16: #Skin
        aRenderer.AddVolume(volumeDict.get(1.5))
    elif v in opacityList:
        opacityList.remove(v)
        aRenderer.RemoveVolume(volumeDict.get(v))
    else:
        aRenderer.AddVolume(volumeDict.get(v))
        opacityList.append(v)
    
    # Camera (viewpoint) settings
    aCamera = vtk.vtkCamera()
    aRenderer.SetActiveCamera(aCamera)
    aCamera.SetPosition(0,0,-1)
    aCamera.Azimuth(-45)
    aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
    # be displayed on starting the visualization
    aCamera.Dolly(1.3)
    
    renWin.Render()
    
def createVolumeDict():
    global colourDict
    #0 is skin colour
    colourDict = {1.5:[1.5,0.0,1.0,0.0],1:[1.0, 0.75, 0.0, 0.0], 2:[2.0, 0.65, 0.65, 0.6], 3:[1.0, 0.75, 0.0, 0.0], 4:[4.0, 1.0, 1.0, 0.0], 
                  5:[1.0, 0.75, 0.0, 0.0], 6:[1.0, 0.75, 0.0, 0.0], 7:[7.0, 0.0, 1.0, 0.0], 8:[1.0, 0.75, 0.0, 0.0], 9:[1.0, 0.75, 0.0, 0.0],
                  10:[10.0, 0.0, 1.0, 1.0], 11:[1.0, 0.75, 0.0, 0.0], 12:[1.0, 0.75, 0.0, 0.0], 13:[13.0, 1.0, 1.0, 1.0], 14:[1.0, 0.75, 0.0, 0.0], 15:[1.0, 0.75, 0.0, 0.0]}
    #[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    global volumeDict
    global lut
    volumeDict = {}

 
       
    
    #opacityTransferFunction = createOpacityTransferFunction([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    
    for value, colourArray in colourDict.iteritems():
        colorTransferFunction = vtk.vtkColorTransferFunction()
        colorTransferFunction.AddRGBPoint(value, colourArray[1], colourArray[2], colourArray[3])
        
        opacityTransferFunction = createOpacityTransferFunction([value])


        #Skin
        if value == 1.5:
            opacityTransferFunction = vtk.vtkPiecewiseFunction()
            opacityTransferFunction.AddPoint(0, 0)
            opacityTransferFunction.AddPoint(1.5, 0.5)
            opacityTransferFunction.AddPoint(3, 0)
        

   # for value, colourArray in colourDict.iteritems():
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
        if value == 1.5:
            volumeMapper.SetInputConnection(readerSkin.GetOutputPort())
        else:
            volumeMapper.SetInputConnection(reader.GetOutputPort())

        
        
        # The volume holds the mapper and the property and
        # can be used to position/orient the volume
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)
        
        volumeDict[value] = volume
    
    print volumeDict


       

if __name__ == "__main__":
    #tissueList = ["Blood", "Brain", "Duodenum", "Eye retina", 
    #              "Eye white", "Heart", "Ileum", "Kidney", "Large intestine",
    #              "Liver", "Lung", "Nerve", "Skeleton", "Spleen", "Stomach"]
    
    global opacityList
    global colorTransferFunction
    global opacityTransferFunction
    global opacityTransferFunctionSkin
    global skinVolume
        
    opacityList = []
    print opacityList
    
    tissueDict = {0: "All", 1: "Blood", 2: "Brain", 3: "Duodenum", 4: "Eye retina", 
                  5: "Eye white", 6: "Heart", 7:"Ileum", 8:"Kidney", 9:"Large intestine",
                  10:"Liver", 11:"Lung", 12:"Nerve", 13:"Skeleton", 14:"Spleen", 15:"Stomach", 16:"Skin"}
    
    #Deze kleuren zijn nog niet allemaal goed. Sommigen zijn dubbel!
    

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
    reader.Update()
    
    readerSkin = vtk.vtkImageReader()
    readerSkin.SetDataExtent(0,499,0,469,1,136)
    readerSkin.SetDataSpacing(1,1,1.5)
    readerSkin.SetDataScalarTypeToUnsignedChar()
    readerSkin.SetFilePattern("./WholeFrog/frog.%s%03d.raw")
    readerSkin.Update()
    
    createVolumeDict()

    Label(root, text="""Choose tissue(s) to visualize:""", justify = LEFT, padx = 20).pack()

    for value, tissue in tissueDict.iteritems():
        var = IntVar()
        
        #All tissues
        if value == 0:
            Checkbutton(root, text=tissue, variable=var, command=lambda v = value: visualizeTissue(v)).pack(side='left')       
        #Skin, change value to 1.5 to find corresponding value in colorDict
        elif value == 16:
            bgColor = '#%02x%02x%02x' % (colourDict.get(1.5)[1]*255, colourDict.get(1.5)[2]*255, colourDict.get(1.5)[3]*255)
            Checkbutton(root, text=tissue, variable=var, bg= bgColor, command=lambda v = value: visualizeTissue(v)).pack(side='left')       
        else:
            bgColor = '#%02x%02x%02x' % (colourDict.get(value)[1]*255, colourDict.get(value)[2]*255, colourDict.get(value)[3]*255)
            Checkbutton(root, text=tissue, variable=var, bg= bgColor, command=lambda v = value: visualizeTissue(v)).pack(side='left')       
        
    
  
#    aRenderer.AddVolume(volumeDict.get(1))
#          
#    aCamera = vtk.vtkCamera()
#    aRenderer.SetActiveCamera(aCamera)
#    aCamera.SetPosition(0,0,-1)
#    aCamera.Azimuth(-45)
#    aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
#    # be displayed on starting the visualization
#    aCamera.Dolly(1.3)
#    
#    renWin.Render()

    root.mainloop()


# root = Tkinter.Tk() 
# aRenderer = vtk.vtkRenderer()
# aRenderer.TexturedBackgroundOn()
# renderWidget = vtkTkRenderWidget(root,width=800,height=600)
# renderWidget.pack(expand='true',fill='both')
# renWin = renderWidget.GetRenderWindow()
# renWin.AddRenderer(aRenderer)
# aRenderer.SetBackground(1, 1, 1)
# renWin.SetSize(600, 480)

# reader = vtk.vtkImageReader()
# reader.SetDataExtent(0,499,0,469,1,136)
# reader.SetDataSpacing(1,1,1.5)
# reader.SetDataScalarTypeToUnsignedChar()
# reader.SetFilePattern("./WholeFrog/frogTissue.%s%03d.raw")
# # reader.SetDataMask(0x7fff)
# reader.Update()

#  # Create transfer mapping scalar value to opacity
# opacityTransferFunction = createOpacityTransferFunction([1,2,7,9,13])
# opacityTransferFunction = createOpacityTransferFunction([1,2,7,9,13])


# # Create transfer mapping scalar value to color
# colorTransferFunction = vtk.vtkColorTransferFunction()
# colorTransferFunction.AddRGBPoint(1.0, 0.75, 0.0, 0.0)
# colorTransferFunction.AddRGBPoint(2.0, 0.65, 0.65, 0.6)

# colorTransferFunction.AddRGBPoint(4.0, 1.0, 1.0, 0.0)
# colorTransferFunction.AddRGBPoint(7.0, 0.0, 1.0, 0.0)
# colorTransferFunction.AddRGBPoint(10.0, 0.0, 1.0, 1.0)
# colorTransferFunction.AddRGBPoint(13.0, 1.0, 1.0, 1.0)
# colorTransferFunction.AddRGBPoint(16.0, 1.0, 0.0, 1.0)

# # The property describes how the data will look
# volumeProperty = vtk.vtkVolumeProperty()
# volumeProperty.SetColor(colorTransferFunction)
# volumeProperty.SetScalarOpacity(opacityTransferFunction)
# # volumeProperty.ShadeOn()
# volumeProperty.SetInterpolationTypeToLinear()

# # The mapper / ray cast function know how to render the data
# compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
# volumeMapper = vtk.vtkVolumeRayCastMapper()
# volumeMapper.SetVolumeRayCastFunction(compositeFunction)
# volumeMapper.SetInputConnection(reader.GetOutputPort())

# # The volume holds the mapper and the property and
# # can be used to position/orient the volume
# volume = vtk.vtkVolume()
# volume.SetMapper(volumeMapper)
# volume.SetProperty(volumeProperty)
# aRenderer.AddVolume(volume)

# # Camera (viewpoint) settings
# aCamera = vtk.vtkCamera()
# aRenderer.SetActiveCamera(aCamera)
# aCamera.SetPosition(0,0,-1)
# aCamera.Azimuth(-45)
# aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
# # be displayed on starting the visualization
# aCamera.Dolly(1.3)

# class scale:
#     "Scale"
#     def __init__(self, root, renWin, volumeProperty):
#         self.renWin, self.volumeProperty = renWin, volumeProperty
#         scale = Tkinter.Scale(root, length=1000, from_=0, to=16,
#                               resolution=.1, orient= "horizontal", 
#                               command=self.change)
#         scale.set(1)  
#         scale.pack(side='bottom')

#     def change(self, val):
#         volumeProperty.SetScalarOpacity(createOpacityTransferFunction([int(float(val))]))
#         self.renWin.Render()


# scale=scale(root, renWin, volumeProperty)

# def callback():
#     volumeProperty.SetScalarOpacity(createOpacityTransferFunction([8]))
#     renWin.Render()

# b = Tkinter.Button(root, text="8", command=callback)
# b.pack()

# root.mainloop()
# >>>>>>> minor changes on assignment 2 and 4



