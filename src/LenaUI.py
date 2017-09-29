"""
The MIT License (MIT)
Copyright (c) 2016 Paul Yoder, Joshua Wade, Kenneth Bailey, Mena Sargios, Joseph Hull, Loraina Lampley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from Tkinter import *
from Batch import Batch
from SeqAnalysis2 import SeqAnalysis

class LenaUI:

    def __init__(self, root):
        self.root = root
        root.title("LENA Contingencies")
        root.geometry('{}x{}'.format(600, 900))
        root.resizable(False, False)

        # create all of the main containers
        top_frame = Frame(root, bg='red', width=600, height=300, pady=3)
        mid_frame = Frame(root, bg='blue', width=600, height=450, pady=3)
        btm_frame = Frame(root, bg='gray', width=600, height=150, pady=3)
        '''
        top_frame = Frame(root, bg='cyan', width=450, height=50, pady=3)
        center = Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
        btm_frame = Frame(root, bg='white', width=450, height=45, pady=3)
        btm_frame2 = Frame(root, bg='lavender', width=450, height=60, pady=3)
        '''

        # layout all of the main containers
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        top_frame.grid(row=0, sticky="ew")
        mid_frame.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")

        '''
        # create the widgets for the top frame
        model_label = Label(top_frame, text='Model Dimensions')
        width_label = Label(top_frame, text='Width:')
        length_label = Label(top_frame, text='Length:')
        entry_W = Entry(top_frame, background="pink")
        entry_L = Entry(top_frame, background="orange")

        # layout the widgets in the top frame
        model_label.grid(row=0, columnspan=3)
        width_label.grid(row=1, column=0)
        length_label.grid(row=1, column=2)
        entry_W.grid(row=1, column=1)
        entry_L.grid(row=1, column=3)

        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        ctr_left = Frame(center, bg='blue', width=100, height=190)
        ctr_mid = Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
        ctr_right = Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

        ctr_left.grid(row=0, column=0, sticky="ns")
        ctr_mid.grid(row=0, column=1, sticky="nsew")
        ctr_right.grid(row=0, column=2, sticky="ns")
        '''