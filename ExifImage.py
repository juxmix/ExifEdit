#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encapsulation of Exif data readed from image file

@author Juanma Sánchez
"""
import os
import logging
from PIL import Image, ExifTags

logging.basicConfig(level=logging.DEBUG)

class ExifImage:
    _imgName = None
    _imgFullName = None
    _exifDict = {}

    def __init__(self, imgName):
        self.loadExif(imgName)

    def loadExif(self, imgName):
        if os.path.isabs(imgName):
            logging.info("[isabs=true] imgName = " + imgName)
            self._imgName = os.path.basename(imgName)
            logging.debug("_imgName: " + self._imgName)
            self._imgFullName = imgName

        else:
            sImgPath = os.path.curdir
            logging.info("sImgPath = " + sImgPath)
            self._imgFullName = sImgPath + os.path.sep + imgName
            logging.info("[isabs=false] _imgFullName: " + self._imgFullName)

        img = Image.open(self._imgFullName)
        try:
            self._exifDict = {
                ExifTags.TAGS.get(k, "Unknown tag ("+str(k)+"):"): v
                for k, v in img._getexif().items()
                #if k in ExifTags.TAGS
            }
            logging.debug("EXIF data:" + str(self._exifDict))
        except AttributeError:
            self._exifDict = None
            logging.error("No readable EXIF data found in: " + self._imgFullName)


