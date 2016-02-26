# -*- coding: utf-8 -*-

from zipfile import ZipFile
from mecab.utils import isPy2x6

def load(fileName):
    """
        Loads the first file from the zip compressed file
    """
    if isPy2x6():
        zipFile = ZipFile(fileName, 'r')
        fileList =  zipFile.namelist()
        if len(fileList) == 0:
            zipFile.close()
            raise IOError('No files in ' + fileName)
        return zipFile.open(fileList[0], 'rU')
    else:
        with ZipFile(fileName, 'r') as zipFile:
            fileList =  zipFile.namelist()
            if len(fileList) == 0:
                raise IOError('No files in ' + fileName)
            return zipFile.open(fileList[0], 'r')