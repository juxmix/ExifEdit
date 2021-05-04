#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Main Window of the Exif editor.
Based on tk technology

@author Juanma Sánchez
"""
import tkinter
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from functools import partial
import logging
from ExifImage import ExifImage

logging.basicConfig(level=logging.INFO)


class MainWindow:
    """ Entry point of the application """

    def __init__(self):
        self._selectedFoto = None
        self._dirSelected = None
        self._iconWidth = 80
        self._iconHeight = 80

        # GUI generals
        self._top = tkinter.Tk()
        self._top.geometry("600x400")

        # GUI elements
        self._frmCampos = tkinter.Frame(self._top)
        self._frmCampos.winfo_toplevel().title("Exif Editor")
        self._frmCampos.pack(side=tkinter.TOP)
        self._lblDir = tkinter.Label(self._frmCampos, text="Carpeta: ")
        self._txtDir = tkinter.Text(self._frmCampos, height=1, width=60)
        self._btnDir = tkinter.Button(self._frmCampos, text="...", command=self.selectDir)
        self._lblDir.grid(column=0, row=1)
        self._txtDir.grid(column=1, row=1)
        self._btnDir.grid(column=2, row=1)

        self._frmFotos = tkinter.Frame(self._top)
        self._frmFotos.pack(side=tkinter.LEFT)
        
        self._frmExif = tkinter.Frame(self._top)
        self._frmExif.pack(side=tkinter.RIGHT)
        
        # go
        self._top.mainloop()

    def selectDir(self):
        # self._top.withdraw()
        self._dirSelected = filedialog.askdirectory()
        logging.debug("DIR: " + self._dirSelected)
        self._txtDir.focus_set()
        self._txtDir.delete(1.0, "end")
        self._txtDir.insert("end", self._dirSelected)
        self.loadImages()

    def getFileName(self, myImage):
        logging.info("Image: " + myImage)

    def getExifData(self, fullName):
        exifImage = ExifImage(fullName)

    def loadImages(self):
        if self._dirSelected != None:
            for myImage in os.listdir(self._dirSelected):
                if myImage.endswith(".jpg"):
                    imgFullName = self._dirSelected + os.path.sep + myImage
                    im = Image.open(imgFullName)
                    im = im.resize((self._iconWidth, self._iconHeight), Image.ANTIALIAS)
                    tkImage = ImageTk.PhotoImage(im)
                    btnImage = tkinter.Button(self._frmFotos, image=tkImage, width=self._iconWidth,
                                              height=self._iconHeight, command=partial(self.getExifData, imgFullName))

                    btnImage.image = tkImage
                    btnImage.pack(side=tkinter.LEFT)


if __name__ == '__main__':
    mw = MainWindow()
