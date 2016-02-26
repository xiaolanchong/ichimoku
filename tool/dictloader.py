import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
#import models

class JDictionary(db.Model):
    kanji = db.StringProperty(indexed=True)
    kana = db.StringProperty(indexed=True)
    entry = db.StringProperty()

class JDictionaryLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'JDictionary',
                                   [('kanji', lambda x: unicode(x, 'utf-8')),
                                    ('kana', lambda x: unicode(x, 'utf-8')),
                                    ('entry', lambda x:unicode(x, 'utf-8'))
									])

loaders = [JDictionaryLoader]