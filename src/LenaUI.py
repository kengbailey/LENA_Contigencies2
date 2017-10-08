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
import platform

MAC = 'Darwin'

class LenaUI:
    "This class is the UI and associated actions"
    def __init__(self, root):
        "UI started on init of class"        
        self.root = root
        root.resizable(False, False)
        root.title("LENA Contingencies")

        # Create main frames
        main_frame = ttk.Frame(root)
        top_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=150)
        mid_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=300)
        btm_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=100)

        # create menu
        menubar = Menu(root) # create menu bar
        root.config(menu=menubar) # attach menubar to root window
        file_menu = Menu(menubar) # create "File" menu item 
        file_menu.add_command(label="Exit", command=self.testing123) # add a command to "File" menu item
        menubar.add_cascade(label="File", menu=file_menu)   # attach "File" menu item to menubar

        # setup main frames to grid
        main_frame.grid(row=0, column=0)
        top_frame.grid(row=0, column=0, sticky=W+E+S+N)
        mid_frame.grid(row=1, column=0, sticky=W+E+S+N)
        btm_frame.grid(row=2, column=0, sticky=W+E+S+N)

        # TOP FRAME CONFIG
        # Create top frame widgets
        csv_var = StringVar()
        txt_var = BooleanVar()
        xl_var = BooleanVar()
        top_dir_label = ttk.Label(top_frame, text="Specify Directory")
        top_reset_btn = ttk.Button(top_frame, text="RESET", command=self.testing123)
        top_load_btn = ttk.Button(top_frame, text="LOAD", command=self.testing123)
        top_input_label = ttk.Label(top_frame, text="Input:")
        top_output_label = ttk.Label(top_frame, text="Output:")
        top_format_label = ttk.Label(top_frame, text="Output Format")        
        top_csv_btn = ttk.Checkbutton(top_frame, text='.csv', command=self.testing123, variable=csv_var,onvalue='this', offvalue='that')
        top_txt_btn = ttk.Checkbutton(top_frame, text=".txt")
        top_xl_btn = ttk.Checkbutton(top_frame, text=".xlsx")
        top_filler = ttk.Label(top_frame, text="      ")
        
        # setup top frame widgets
        top_reset_btn.grid(row=0, column=4, sticky=E)
        top_dir_label.grid(row=1, column=0, columnspan=2, sticky=N)
        top_input_label.grid(row=2, column=0)
        top_output_label.grid(row=3, column=0)
        top_format_label.grid(row=5, column=0, columnspan=2)
        top_filler.grid(row=4, column=0)
        top_csv_btn.grid(row=6, column=0)
        top_txt_btn.grid(row=6, column=1)
        top_xl_btn.grid(row=6, column=2)
        top_load_btn.grid(row=0, column=3)

        # MID FRAME CONFIG
        # create mid frame widgets
        type_var = StringVar()
        ab_a_var = StringVar()
        ab_b_var = StringVar()
        abc_a_var = StringVar()
        abc_b_var = StringVar()
        abc_c_var = StringVar()
        mid_type_label = ttk.Label(mid_frame, text=' Type of Analysis')       
        mid_ab_btn = ttk.Radiobutton(mid_frame, text='A ---> B', variable=type_var, value='ab')
        mid_abc_btn = ttk.Radiobutton(mid_frame, text='( A ---> B ) ---> C', variable=type_var, value='abc')        
        mid_filler_label = ttk.Label(mid_frame, text="     ")
        mid_conf_label = ttk.Label(mid_frame, text="Configure Analysis")
        mid_ab_a_btn = ttk.Combobox(mid_frame, textvariable=ab_a_var, width=3)
        mid_ab_b_btn = ttk.Combobox(mid_frame, textvariable=ab_b_var, width=3)
        mid_abc_a_btn = ttk.Combobox(mid_frame, textvariable=abc_a_var, width=3)
        mid_abc_b_btn = ttk.Combobox(mid_frame, textvariable=abc_b_var, width=3)
        mid_abc_c_btn = ttk.Combobox(mid_frame, textvariable=abc_c_var, width=3)
        mid_filler_label2 = ttk.Label(mid_frame, text="-----")
        mid_filler_label3 = ttk.Label(mid_frame, text="      ")

        # setup mid frame widgets
        mid_type_label.grid(row=0, column=0, columnspan=3)
        mid_ab_btn.grid(row=1, column=0, columnspan=2)
        mid_abc_btn.grid(row=2, column=0, columnspan=3)
        mid_filler_label.grid(row=3, column=0, columnspan=3)
        mid_conf_label.grid(row=4, column=0, columnspan=3)
        mid_ab_a_btn.grid(row=5, column=0)
        mid_ab_b_btn.grid(row=5, column=1)
        mid_abc_a_btn.grid(row=5, column=3)
        mid_abc_b_btn.grid(row=5, column=4)
        mid_filler_label2.grid(row=5, column=2)
        mid_abc_c_btn.grid(row=5, column=5)
        mid_filler_label.grid(row=6, column=0, columnspan=3)

        # OSX ONLY - bring window to front
        if platform.system() == MAC:
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def testing123(event):
        print("testing 123...")