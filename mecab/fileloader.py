# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import io
import sys
import os.path
from . import compress

class FileLoader:
    def __init__(self, fileNames, dataDirectory):
        self.fileNames = fileNames
        self.dataDirectory = dataDirectory

    def load(self, fileNameNoExt):
        ext = self.fileNames.get(fileNameNoExt)
        if ext is None:
            raise RuntimeError("'{0}' is not in the file name map".format(fileNameNoExt))
        if ext == 'zip':
            fullName = os.path.join(self.dataDirectory, fileNameNoExt + '.' + ext)
            return compress.load(fullName)
        elif ext == 'bin':
            fullName = os.path.join(self.dataDirectory, fileNameNoExt + '.' + ext)
            return io.open(fullName, 'rb')
        elif len(ext) == 2 and ext == 'txt':
            fullName = os.path.join(self.dataDirectory, fileNameNoExt + '.' + ext[0])
            encoding = ext[1]
            return io.open(fullName, encoding = encoding)
        else:
            raise RuntimeError(ext + ": unknown file extention")
