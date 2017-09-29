"""
The MIT License (MIT)
Copyright (c) 2017 Paul Yoder, Joshua Wade, Kenneth Bailey, Mena Sargios, Joseph Hull, Loraina Lampley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import ttk
from Tkinter import *
from Batch import Batch
from SeqAnalysis2 import SeqAnalysis
import os

class LenaUI:

    def __init__(self, root):
        self.root = root
        root.title("LENA Contingencies")
        root.geometry('{}x{}'.format(500, 700))
        root.resizable(False, False)
        
        # create all of the main containers
        top_frame = Frame(root, bg='white', width=500, height=300)
        mid_frame = Frame(root, bg='white', width=500, height=300)
        btm_frame = Frame(root, bg='white', width=500, height=100)

        # layout main containers
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # layout 
        top_frame.grid(row=0, sticky="ew")
        mid_frame.grid(row=1, sticky="nsew")
        btm_frame.grid(row=2, sticky="ew")

        # OSX ONLY - bring window to front
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')