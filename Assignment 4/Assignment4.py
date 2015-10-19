

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
class Tissue(object):

    def __init__(self, name, val, colour):
        self.name = name
        self.val = val
        self.R = colour[0]
        self.G = colour[1]
        self.B = colour[2]
        self.opacity = 0
        self.check = None

    def setOpacity(self, v):
        self.opacity = v

    def setCheck(self, check):
        self.check = check

def createOTF(tissues):
    OTF = vtk.vtkPiecewiseFunction()
    OTF.AddPoint(0, 0)
    for t in tissues:
        OTF.AddPoint(t.val - 0.5, 0)
        OTF.AddPoint(t.val, t.opacity)
        OTF.AddPoint(t.val + 0.5, 0)
    OTF.AddPoint(17.0, 0)
    return OTF

def createSkinOTF(tissues):
    skinOTF = vtk.vtkPiecewiseFunction()
    skinOTF.AddPoint(70, 0)
    skinOTF.AddPoint(80, tissues[15].opacity *.5)
    skinOTF.AddPoint(90, tissues[15].opacity *.5)
    skinOTF.AddPoint(100.0, 0)
    return skinOTF

def createCTF(tissues):  
    CTF = vtk.vtkColorTransferFunction()
    for tissue in tissues:
        CTF.AddRGBPoint(tissue.val, tissue.R, tissue.G, tissue.B)
    return CTF

def createSkinCTF(tissues):
    skinCTF = vtk.vtkColorTransferFunction()
    skinCTF.AddRGBPoint(1, 0,0,0)
    skinCTF.AddRGBPoint(2, tissues[15].R, tissues[15].G, tissues[15].B)
    skinCTF.AddRGBPoint(255, tissues[15].R, tissues[15].G, tissues[15].B)
    return skinCTF


def update(tissues, tissue, opacityDict):
    tissue.setOpacity(opacityDict[tissue].get())

    if tissue.name == "Skin":
        print tissue.name
        skinOTF = createSkinOTF(tissues)
        skinVolumeProperty.SetScalarOpacity(skinOTF)

    else:
        OTF = createOTF(tissues)
        volumeProperty.SetScalarOpacity(OTF)

    renWin.Render()
   
def selectAllTissues(tissues):
    for t in tissues:
        t.check.select()
        t.setOpacity(.1)
    OTF = createOTF(tissues)
    volumeProperty.SetScalarOpacity(OTF)
    skinOTF = createSkinOTF(tissues)
    skinVolumeProperty.SetScalarOpacity(skinOTF)
    renWin.Render()

def deselectAllTissues(tissues):
    for t in tissues:
        t.check.deselect()
        t.setOpacity(0)
    OTF = createOTF(tissues)
    volumeProperty.SetScalarOpacity(OTF)
    skinOTF = createSkinOTF(tissues)
    skinVolumeProperty.SetScalarOpacity(skinOTF)
    renWin.Render() 

if __name__ == "__main__":
    tissues = [
        Tissue("Blood", 1, [0.75, 0.0, 0.0]), 
        Tissue("Brain", 2, [0.65, 0.65, 0.6]), 
        Tissue("Duodenum", 3, [0.75, 0.75, 0.0]), 
        Tissue("Eye retina", 4, [1.0, 0.4, 0.0]), 
        Tissue("Eye white", 5, [1, 1, 1]), 
        Tissue("Heart", 6, [0.4, 0.0, 0.0]), 
        Tissue("Ileum", 7, [0.6, 0.3, 0.15]), 
        Tissue("Kidney", 8, [0.40, 0.3, 0.2]), 
        Tissue("Large intestine", 9, [0.80, 0.20, 0.20]),
        Tissue("Liver", 10, [0.0, 1.0, 1.0]), 
        Tissue("Lung", 11, [0.1, 0.1, 0.1]),
        Tissue("Nerve", 12, [0.0, 0.8, 0.3]),
        Tissue("Skeleton", 13, [.9, .9, .9]),
        Tissue("Spleen", 14, [0.75, 0.0, 0.85]),
        Tissue("Stomach", 15, [0.6, 0.6, 0.2]), 
        Tissue("Skin", 16, [0.20, 0.40, 0.0])
        ]


    root = Tkinter.Tk() 
    aRenderer = vtk.vtkRenderer()
    aRenderer.GradientBackgroundOn()
    aRenderer.SetBackground(0,0,0)
    aRenderer.SetBackground2(0,0,.1)
    renderWidget = vtkTkRenderWidget(root,width=800,height=600)
    renderWidget.grid(column=0, rowspan=len(tissues) + 4)
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

    # create color transfer function (static)
    CTF = createCTF(tissues)
    skinCTF = createSkinCTF(tissues)
    # create OTF (dynamic by changing checkboxes)
    OTF = createOTF(tissues)
    skinOTF = createSkinOTF(tissues)



    # The property describes how the data will look
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(CTF)
    volumeProperty.SetScalarOpacity(OTF)
    volumeProperty.SetInterpolationTypeToLinear()

    skinVolumeProperty = vtk.vtkVolumeProperty()
    skinVolumeProperty.SetColor(skinCTF)
    skinVolumeProperty.SetScalarOpacity(skinOTF)
    # skinVolumeProperty.ShadeOn()
    skinVolumeProperty.SetInterpolationTypeToLinear()

    # The mapper / ray cast function know how to render the data
    compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(compositeFunction)
    volumeMapper.SetInputConnection(reader.GetOutputPort())
    
    skinCompositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    skinVolumeMapper = vtk.vtkVolumeRayCastMapper()
    skinVolumeMapper.SetVolumeRayCastFunction(skinCompositeFunction)
    skinVolumeMapper.SetInputConnection(readerSkin.GetOutputPort())


    # The volume holds the mapper and the property and
    # can be used to position/orient the volume
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    skinVolume = vtk.vtkVolume()
    skinVolume.SetMapper(skinVolumeMapper)
    skinVolume.SetProperty(skinVolumeProperty)

    aRenderer.AddVolume(volume)
    aRenderer.AddVolume(skinVolume)
         
    aCamera = vtk.vtkCamera()
    aRenderer.SetActiveCamera(aCamera)
    aCamera.SetPosition(0,0,-1)
    aCamera.Azimuth(-25)
    aCamera.Roll(90)
    aRenderer.ResetCamera() #Without this camera Reset, the actors will not 
    # be displayed on starting the visualization
    aCamera.Dolly(1.3)

    renWin.Render()

    Label(root, text="""Choose tissue(s) to visualize:""", justify = LEFT, padx = 20).grid(row = 0, rowspan=2, column=1)
    varDict = {}
    for tissue in tissues:
        varDict[tissue] = DoubleVar()
        varDict[tissue].set(0)
        bgColour = '#%02x%02x%02x' % (tissue.R * 255, tissue.G * 255, tissue.B * 255)
        tissue.setCheck(Checkbutton(root, text=tissue.name, offvalue = 0, onvalue = .1, variable = varDict[tissue], bg= bgColour, 
            command=lambda tissue = tissue: update(tissues, tissue, varDict)))
        tissue.check.grid(row=tissue.val + 3, column=1, columnspan = 2, sticky="w", padx = 10)


    Button(root, text = "All Tissues", command=lambda tissues = tissues: selectAllTissues(tissues) ).grid(column=1, row=2, sticky="w")
    Button(root, text = "No Tissues", command=lambda tissues = tissues: deselectAllTissues(tissues) ).grid(column=2, row=2, sticky="w")

    
    root.mainloop()


