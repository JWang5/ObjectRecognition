# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:57:55 2020

@author: jiayi
"""

from nbformat import v3, v4

with open("arid.py") as fpin:
    
    text = fpin.read()
    text += """
# <markdowncell>

# If you can read this, reads_py() is no longer broken! 
"""

nbook = v3.reads_py(text)
nbook = v4.upgrade(nbook)  # Upgrade v3 to v4

jsonform = v4.writes(nbook) + "\n"
with open("arid.ipynb", "w") as fpout:
    fpout.write(jsonform)