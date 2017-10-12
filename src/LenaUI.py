"""
The MIT License (MIT)
Copyright (c) 2017 Paul Yoder, Joshua Wade, Kenneth Bailey, Mena Sargios, Joseph Hull, Loraina Lampley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import ttk, tkFileDialog
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
        main_frame = ttk.Frame(root) # top, mid, btm frames embedded within this frame
        self.top_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=150)
        self.mid_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=300)
        self.btm_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=100)

        # create menu
        menubar = Menu(root) # create menu bar
        root.config(menu=menubar) # attach menubar to root window

        # file menu
        file_menu = Menu(menubar) # create "File" menu item 
        file_menu.add_command(label="Exit", command=self.testing123) # add a command to "File" menu item
        menubar.add_cascade(label="File", menu=file_menu)   # attach "File" menu item to menubar
        
        # help menu
        help_menu = Menu(menubar) # create "Help" menu item 
        help_menu.add_command(label="Instructions", command=self.testing123) # add a command to "Help" menu item
        menubar.add_cascade(label="Help", menu=help_menu) # attach "Help" menu item to helpbar

        # setup main frames to grid
        # top, mid, btm frames laid out inside main_frame
        # sticky tags used to keep UI elements together when stretched
        main_frame.grid(row=0, column=0) 
        self.top_frame.grid(row=0, column=0, sticky=W+E+S+N)
        self.mid_frame.grid(row=1, column=0, sticky=W+E+S+N)
        self.btm_frame.grid(row=2, column=0, sticky=W+E+S+N)

        # Setup Individual Frames
        self.setup_top_frame()
        self.setup_mid_frame()
        self.setup_btm_frame()

        # OSX ONLY - bring window to front
        if platform.system() == MAC:
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def testing123(event):
        print("testing 123...")
        print(event)

    def setup_top_frame(self):
        # TOP FRAME CONFIG
        # Create top frame widgets
        in_path_var = StringVar()   # holds path for input directory //J
        out_path_var = StringVar()  # holds path for output directory   //J
        csv_var = BooleanVar() # holds user selection for csv output
        txt_var = BooleanVar() # holds user selection for txt output
        xl_var = BooleanVar()  # holds user selection for xlsx output

        top_dir_label = ttk.Label(self.top_frame, text="Specify Directory")
        top_reset_btn = ttk.Button(self.top_frame, text="RESET", command=self.testing123)
        top_load_btn = ttk.Button(self.top_frame, text="LOAD", command=self.testing123)
        top_input_label = ttk.Label(self.top_frame, text="   Input:")
        top_output_label = ttk.Label(self.top_frame, text="Output:")
        top_format_label = ttk.Label(self.top_frame, text="Output Format")        
        top_csv_btn = ttk.Checkbutton(self.top_frame, text='.csv', command=self.testing123, variable=csv_var,onvalue=1, offvalue=0)
        top_txt_btn = ttk.Checkbutton(self.top_frame, text=".txt", command=self.testing123, variable=txt_var,onvalue=1, offvalue=0)
        top_xl_btn = ttk.Checkbutton(self.top_frame, text=".xlsx", command=self.testing123, variable=xl_var,onvalue=1, offvalue=0)
        top_filler = ttk.Label(self.top_frame, text="      ")
        top_in_browse_btn = ttk.Button(self.top_frame, text="Browse...", command=tkFileDialog.askdirectory)    #Browse button for input directory //J
        top_out_browse_btn = ttk.Button(self.top_frame, text="Browse...", command=tkFileDialog.askdirectory)   #Browse button for output directory //J
        top_in_path = Entry(self.top_frame, width=20, textvariable=in_path_var, state=DISABLED)     #create the label to display input directory path //J      
        top_out_path = Entry(self.top_frame, width=20, textvariable=out_path_var, state=DISABLED)   #create the label to display output directory path //J
        
        # setup top frame widgets
        top_reset_btn.grid(row=0, column=4, sticky=E)
        top_dir_label.grid(row=1, column=0, columnspan=2, sticky=N)
        top_input_label.grid(row=2, column=0)
        top_output_label.grid(row=3, column=0)
        top_in_browse_btn.grid(row=2, column=1) #
        top_out_browse_btn.grid(row=3, column=1)#
        top_in_path.grid(row=2, column=2, columnspan=2) #
        top_out_path.grid(row=3, column=2, columnspan=2)#
        
        top_format_label.grid(row=5, column=0, columnspan=2)
        top_filler.grid(row=4, column=0)
        top_csv_btn.grid(row=6, column=0)
        top_txt_btn.grid(row=6, column=1)
        top_xl_btn.grid(row=6, column=2)
        top_load_btn.grid(row=0, column=3)

    def setup_mid_frame(self):
        # MID FRAME CONFIG
        # create mid frame widgets
        codes = ['MAN','MAF','FAN','FAF','CHNSP','CHNNSP', \
			'CHF','CXN','CXF','NON','NOF','OLN','OLF','TVN', \
			'TVF','SIL']
        type_var = StringVar()
        ab_a_var = StringVar()
        ab_b_var = StringVar()
        abc_a_var = StringVar()
        abc_b_var = StringVar()
        abc_c_var = StringVar()
        pause_var = BooleanVar()
        mid_type_label = ttk.Label(self.mid_frame, text='Type of Analysis')       
        mid_ab_btn = ttk.Radiobutton(self.mid_frame, text='A ---> B', variable=type_var, value='ab')
        mid_abc_btn = ttk.Radiobutton(self.mid_frame, text='( A ---> B ) ---> C', variable=type_var, value='abc')        
        mid_filler_label = ttk.Label(self.mid_frame, text="     ")
        mid_conf_label = ttk.Label(self.mid_frame, text="Configure Analysis")
        mid_conf_ab_a_label = ttk.Label(self.mid_frame, text="A") 
        mid_conf_ab_b_label = ttk.Label(self.mid_frame, text="B") 
        mid_conf_abc_a_label = ttk.Label(self.mid_frame, text="A") 
        mid_conf_abc_b_label = ttk.Label(self.mid_frame, text="B") 
        mid_conf_abc_c_label = ttk.Label(self.mid_frame, text="C") 
        mid_ab_a_btn = ttk.Combobox(self.mid_frame, textvariable=ab_a_var, width=8)
        mid_ab_a_btn['values'] = codes
        mid_ab_b_btn = ttk.Combobox(self.mid_frame, textvariable=ab_b_var, width=8)
        mid_ab_b_btn['values'] = codes
        mid_abc_a_btn = ttk.Combobox(self.mid_frame, textvariable=abc_a_var, width=8)
        mid_abc_a_btn['values'] = codes
        mid_abc_b_btn = ttk.Combobox(self.mid_frame, textvariable=abc_b_var, width=8)
        mid_abc_b_btn['values'] = codes
        mid_abc_c_btn = ttk.Combobox(self.mid_frame, textvariable=abc_c_var, width=8)
        mid_abc_c_btn['values'] = codes   
        mid_filler_label2 = ttk.Label(self.mid_frame, text="     ")
        mid_pause_label = ttk.Label(self.mid_frame, text="Pause Duration")
        mid_filler_label3 = ttk.Label(self.mid_frame, text="     ")
        mid_pause_slider = ttk.Scale(self.mid_frame, orient=HORIZONTAL, length=100, from_=1.0, to=50.0)
        mid_pause_dn_btn = ttk.Button(self.mid_frame, text="<", command=self.testing123, width=2)
        mid_pause_up_btn = ttk.Button(self.mid_frame, text=">", command=self.testing123, width=2)
        mid_pause_entry = ttk.Entry(self.mid_frame, width=3)
        mid_pause_checkbox = ttk.Checkbutton(self.mid_frame, text="Enable rounding", command=self.testing123)
        
        # setup mid frame widgets
        mid_type_label.grid(row=0, column=1, columnspan=3)
        mid_ab_btn.grid(row=2, column=0, columnspan=3, sticky = W)
        mid_abc_btn.grid(row=8, column=0, columnspan=3, sticky = W)
        #mid_conf_label.grid(row=1, column=1, columnspan=4)
        mid_conf_ab_a_label.grid(row=4, column=0)
        mid_conf_ab_b_label.grid(row=4, column=1)
        mid_conf_abc_a_label.grid(row=9, column=0)
        mid_conf_abc_b_label.grid(row=9, column=1)
        mid_conf_abc_c_label.grid(row=9, column=2)
        mid_ab_a_btn.grid(row=5, column=0)
        mid_ab_b_btn.grid(row=5, column=1)
        mid_abc_a_btn.grid(row=10, column=0)
        mid_abc_b_btn.grid(row=10, column=1)
        mid_filler_label2.grid(row=7, column=2)
        mid_abc_c_btn.grid(row=10, column=2)
        mid_filler_label3.grid(row=12, column=0, columnspan=3)
        mid_pause_label.grid(row=13, column=1, columnspan=3)
        mid_pause_slider.grid(row=14, column=1, columnspan=3)
        mid_pause_dn_btn.grid(row=14, column=4)
        mid_pause_up_btn.grid(row=14, column=5)
        mid_pause_entry.grid(row=14, column=0, sticky = E)
        mid_pause_checkbox.grid(row=15, column=1, columnspan=3)

    def setup_btm_frame(self):
        # BOTTOM FRAME CONFIG
        # create bottom frame widgets
        btm_submit_btn = ttk.Button(self.btm_frame, text="Submit", command=self.testing123)
        btm_progress_bar = ttk.Progressbar(self.btm_frame, orient=HORIZONTAL, length=200, mode='determinate')
        btm_text_window = Text(self.btm_frame, width=50, height=3)

        # arrange bottom frame widgets
        btm_submit_btn.grid(row=0, column=0)
        btm_progress_bar.grid(row=0, column=1)
        btm_text_window.grid(row=1, column=0, columnspan=2)