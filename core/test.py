# -*- coding: utf-8 -*-
import os

rootDir = '/home/benny/Workspaces/markipydia/miki2/wiki/'
print rootDir
if rootDir[-1]=='/':
    rootDir = rootDir[:-1]
exportdir = os.path.join(os.path.dirname(rootDir),'html/')
print exportdir
for dirName, subdirList, fileList in os.walk(rootDir):
    relDir = os.path.relpath(dirName, rootDir)
    for fname in fileList:
        mdf = os.path.join(dirName,fname)
        print mdf
        print os.path.join(exportdir, os.path.relpath(mdf, rootDir))



"""
import markdown
from docdata.mmddata import get_data

mdfpath = '/home/benny/Workspaces/markipydia/miki2/wiki/index.md'

with open(mdfpath, 'r') as f:
    doc = f.read()
    doc, data = get_data(doc)
#print doc
print data
doc = doc.decode('utf-8')

md = markdown.Markdown(extensions=['markdown.extensions.toc'])
html = md.convert(doc)
toc = md.toc
print html
print toc
"""

import yaml
doc = """
  a: 1
  b:
    c: 3
    d: 4
"""
print type(yaml.load(doc))
