#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encapsulation of Exif data readed from image file

@author Juanma Sánchez
"""
import os
import logging
from PIL import Image, ExifTags
import datetime
from fractions import Fraction

logging.basicConfig(level=logging.DEBUG)

class ExifImage:
    _imgName = None
    _imgFullName = None
    _exifDictStandard = {}
    _exifDictUserDefined = {}

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
            exifDataPIL = img._getexif()

            #self._exifDict = {
            #    ExifTags.TAGS.get(k, "User defined ("+str(k)+"):"): v
            #    for k, v in img._getexif().items()
            #    #if k in ExifTags.TAGS
            #}
            # Load all standard values first (even nonexisting in image)
            for k, v in ExifTags.TAGS.items():
                if k in exifDataPIL:
                    value = exifDataPIL[k]
                else:
                    value = None

                self._exifDictStandard[v] = {"tag": k,
                                     "raw": value,
                                     "processed": value}
            # Nonstandard values also
            for k, v in exifDataPIL.items():
                if k not in ExifTags.TAGS.items():
                    self._exifDictUserDefined[k] = {
                        "tag": k,
                        "raw": v,
                        "processed": v
                    }

            self._exifDictStandard = self._processExifData(self._exifDictStandard)
            logging.debug("EXIF standard data:" + str(self._exifDictStandard))
            logging.debug("EXIF User data:" + str(self._exifDictUserDefined))
        except (AttributeError, TypeError):
            self._exifDictStandard = None
            self._exifDictUserDefined = None
            logging.error("No readable EXIF data found in: " + self._imgFullName)

    def _processExifData(self, stdExifDict):
        date_format = "%Y:%m:%d %H:%M:%S"

        lookups = self._create_lookups()


        if stdExifDict["DateTime"]["raw"] != None:
            stdExifDict["DateTime"]["processed"] = \
                datetime.datetime.strptime(stdExifDict["DateTime"]["raw"], date_format)


        if stdExifDict["DateTimeOriginal"]["raw"] != None:
            stdExifDict["DateTimeOriginal"]["processed"] = \
                datetime.datetime.strptime(stdExifDict["DateTimeOriginal"]["raw"], date_format)

        if stdExifDict["DateTimeDigitized"]["raw"] != None:
            stdExifDict["DateTimeDigitized"]["processed"] = \
                datetime.datetime.strptime(stdExifDict["DateTimeDigitized"]["raw"], date_format)

        if stdExifDict["FNumber"]["raw"] != None:
            stdExifDict["FNumber"]["processed"] = \
                self._derationalize(stdExifDict["FNumber"]["raw"])

        if stdExifDict["FNumber"]["processed"] != None:
            stdExifDict["FNumber"]["processed"] = \
                "f{}".format(stdExifDict["FNumber"]["raw"])

        if stdExifDict["MaxApertureValue"]["raw"] != None:
            stdExifDict["MaxApertureValue"]["processed"] = \
                self._derationalize(stdExifDict["MaxApertureValue"]["raw"])

        if stdExifDict["MaxApertureValue"]["processed"] != None:
            stdExifDict["MaxApertureValue"]["processed"] = \
                "f{:2.1f}".format(stdExifDict["MaxApertureValue"]["processed"])

        if stdExifDict["FocalLength"]["raw"] != None:
            stdExifDict["FocalLength"]["processed"] = \
                self._derationalize(stdExifDict["FocalLength"]["raw"])

        if stdExifDict["FocalLength"]["processed"] != None:
            stdExifDict["FocalLength"]["processed"] = \
                "{}mm".format(stdExifDict["FocalLength"]["raw"])

        if stdExifDict["FocalLengthIn35mmFilm"]["raw"] != None:
            stdExifDict["FocalLengthIn35mmFilm"]["processed"] = \
                "{}mm".format(stdExifDict["FocalLengthIn35mmFilm"]["raw"])

        if stdExifDict["Orientation"]["raw"] != None:
            stdExifDict["Orientation"]["processed"] = \
                lookups["orientations"][stdExifDict["Orientation"]["raw"]]

        if stdExifDict["ResolutionUnit"]["raw"] != None:
            stdExifDict["ResolutionUnit"]["processed"] = \
                lookups["resolution_units"][stdExifDict["ResolutionUnit"]["raw"]]

        if stdExifDict["ExposureProgram"]["raw"] != None:
            stdExifDict["ExposureProgram"]["processed"] = \
                lookups["exposure_programs"][stdExifDict["ExposureProgram"]["raw"]]

        if stdExifDict["MeteringMode"]["raw"] != None:
            stdExifDict["MeteringMode"]["processed"] = \
                lookups["metering_modes"][stdExifDict["MeteringMode"]["raw"]]

        if stdExifDict["XResolution"]["raw"] != None:
            stdExifDict["XResolution"]["processed"] = \
                int(self._derationalize(stdExifDict["XResolution"]["raw"]))

        if stdExifDict["YResolution"]["raw"] != None:
            stdExifDict["YResolution"]["processed"] = \
                int(self._derationalize(stdExifDict["YResolution"]["raw"]))

        if stdExifDict["ExposureTime"]["raw"] != None:
            stdExifDict["ExposureTime"]["processed"] = \
                self._derationalize(stdExifDict["ExposureTime"]["raw"])

        if stdExifDict["ExposureTime"]["processed"] != None:
            stdExifDict["ExposureTime"]["processed"] = \
                str(Fraction(stdExifDict["ExposureTime"]["processed"]).limit_denominator(8000))

        if stdExifDict["ExposureBiasValue"]["raw"] != None:
            stdExifDict["ExposureBiasValue"]["processed"] = \
                self._derationalize(stdExifDict["ExposureBiasValue"]["raw"])

        if stdExifDict["ExposureBiasValue"]["processed"] != None:
            stdExifDict["ExposureBiasValue"]["processed"] = \
                "{} EV".format(stdExifDict["ExposureBiasValue"]["raw"])

        return stdExifDict

    def _create_lookups(self):
        lookups = {}

        lookups["metering_modes"] = ("Undefined",
                                 "Average",
                                 "Center-weighted average",
                                 "Spot",
                                 "Multi-spot",
                                 "Multi-segment",
                                 "Partial")

        lookups["exposure_programs"] = ("Undefined",
                                    "Manual",
                                    "Program AE",
                                    "Aperture-priority AE",
                                    "Shutter speed priority AE",
                                    "Creative (Slow speed)",
                                    "Action (High speed)",
                                    "Portrait ",
                                    "Landscape",
                                    "Bulb")

        lookups["resolution_units"] = ("",
                                   "Undefined",
                                   "Inches",
                                   "Centimetres")

        lookups["orientations"] = ("",
                               "Horizontal",
                               "Mirror horizontal",
                               "Rotate 180",
                               "Mirror vertical",
                               "Mirror horizontal and rotate 270 CW",
                               "Rotate 90 CW",
                               "Mirror horizontal and rotate 90 CW",
                               "Rotate 270 CW")

        return lookups

    def _derationalize(self, rational):
        return rational[0] / rational[1]