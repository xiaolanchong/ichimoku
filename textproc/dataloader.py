import os.path
from mecab.fileloader import FileLoader

def getDataLoader():
    dataDir = os.path.join(os.path.dirname(__file__), '..')
    dataDir = os.path.abspath(dataDir)
    dataDir = os.path.join(dataDir, 'data')
    dataExt =  \
    {
        'sys' : 'zip',
        'unk' : 'zip',
        'jdict' : 'zip',
        'matrix': 'bin',
        'char' : 'bin',
    }
    return FileLoader(dataExt, dataDir)
