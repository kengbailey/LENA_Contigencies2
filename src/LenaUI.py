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
import threading
import time

MAC = 'Darwin'
OK = 'ok'
AB = 'A_B'
ABC = 'AB_C'

class LenaUI:

    "This class is the UI and associated actions"
    def __init__(self, root):
        "UI started on init of class"        
        self.root = root
        root.resizable(False, False)
        root.title("LENA Contingencies")

        # Class Attributes
        self.its_file_dict = {} # k:ID v:path/to/file
        self.seq_config = {}
        self.input_dir = StringVar()
        self.output_dir = StringVar()
        self.pause_duration = None
        self.rounding_enabled = False
        self.sequence_type = None
        self.var_a = None
        self.var_b = None
        self.var_c = None
        self.output_format = []
        

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

    def testing123(self, event):
        print("testing 123...")
        print(event)

    def change_pause_legnthU(self, event, pause_length_var):
        if pause_length_var.get() < 50.0:
            pause_length_var.set(pause_length_var.get()+0.1)

    def change_pause_lengthD(self, event, pause_length_var):
        if pause_length_var.get() >= 1.0:
            pause_length_var.set(pause_length_var.get()-0.1)

    def setup_top_frame(self):
        # TOP FRAME CONFIG
        # Create top frame widgets
        csv_var = BooleanVar() # holds user selection for csv output
        txt_var = BooleanVar() # holds user selection for txt output
        xl_var = BooleanVar()  # holds user selection for xlsx output

        top_dir_label = ttk.Label(self.top_frame, text="Specify Directory")
        top_reset_btn = ttk.Button(self.top_frame, text="RESET", command=self.testing123)
        top_load_btn = ttk.Button(self.top_frame, text="LOAD", command=self.testing123)
        top_input_label = ttk.Label(self.top_frame, text="Input:")
        top_output_label = ttk.Label(self.top_frame, text="Output:")
        top_format_label = ttk.Label(self.top_frame, text="Output Format")        
        top_csv_btn = ttk.Checkbutton(self.top_frame, text='.csv', command=self.testing123, variable=csv_var,onvalue=1, offvalue=0)
        top_txt_btn = ttk.Checkbutton(self.top_frame, text=".txt", command=self.testing123, variable=txt_var,onvalue=1, offvalue=0)
        top_xl_btn = ttk.Checkbutton(self.top_frame, text=".xlsx", command=self.testing123, variable=xl_var,onvalue=1, offvalue=0)
        top_filler = ttk.Label(self.top_frame, text="      ")
        top_in_browse_btn = ttk.Button(self.top_frame, text="Browse...", command=self.select_input_dir)    #Browse button for input directory //J
        top_out_browse_btn = ttk.Button(self.top_frame, text="Browse...", command=self.select_output_dir)   #Browse button for output directory //J
        self.top_in_path = Entry(self.top_frame, width=20, textvariable=self.input_dir, state=DISABLED)     #create the label to display input directory path //J      
        self.top_out_path = Entry(self.top_frame, width=20, textvariable=self.output_dir, state=DISABLED)   #create the label to display output directory path //J
        
        # setup top frame widgets
        top_reset_btn.grid(row=0, column=3, sticky=E)
        top_dir_label.grid(row=1, column=0, columnspan=2, sticky=N)
        top_input_label.grid(row=2, column=0, sticky=E)
        top_output_label.grid(row=3, column=0, sticky=E)
        top_in_browse_btn.grid(row=2, column=3) #
        top_out_browse_btn.grid(row=3, column=3)#
        self.top_in_path.grid(row=2, column=1, columnspan=2) #
        self.top_out_path.grid(row=3, column=1, columnspan=2)#
        
        top_format_label.grid(row=5, column=0, columnspan=2)
        top_filler.grid(row=4, column=0)
        top_csv_btn.grid(row=6, column=0)
        top_txt_btn.grid(row=6, column=1)
        top_xl_btn.grid(row=6, column=2)
        top_load_btn.grid(row=0, column=2)

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
        pause_length_var = DoubleVar()
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
        mid_pause_slider = ttk.Scale(self.mid_frame, orient=HORIZONTAL, length=100, from_=1.0, to=50.0, variable=pause_length_var)
        mid_pause_dn_btn = ttk.Button(self.mid_frame, text="<", command=lambda: self.change_pause_lengthD(self,pause_length_var), width=2)
        mid_pause_up_btn = ttk.Button(self.mid_frame, text=">", command=lambda: self.change_pause_legnthU(self,pause_length_var), width=2)
        mid_pause_entry = ttk.Entry(self.mid_frame, textvariable=pause_length_var, width=3)
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
        btm_submit_btn = ttk.Button(self.btm_frame, text="Submit", command=self.run_seqanalysis)
        btm_progress_bar = ttk.Progressbar(self.btm_frame, orient=HORIZONTAL, length=200, mode='determinate')
        btm_text_window = Text(self.btm_frame, width=50, height=3)

        # arrange bottom frame widgets
        btm_submit_btn.grid(row=0, column=0)
        btm_progress_bar.grid(row=0, column=1)
        btm_text_window.grid(row=1, column=0, columnspan=2)


    def select_input_dir(self):
        self.input_dir.set(tkFileDialog.askdirectory())

    def select_output_dir(self):
        self.output_dir.set(tkFileDialog.askdirectory())

    def get_its_files(self):
        "This method looks creates a dict of all .its files found in the input directory"
        self.its_file_dict = Batch(self.input_dir)

    def check_config(self):
        "This method checks if all seq_config values are set. Returns error message if any aren't set."

        # Error messages stored here
        error = ""

        # check input directory
        if len(self.input_dir) < 1:
            error += "Input directory not set! "
        
        # check output directory
        if len(self.output_dir) < 1:
            error += "Output directory not set! "
        
        # check var_a
        if self.var_a is None:
            error += "A is not set! "

        # check var_b
        if self.var_b is None:
            error += "B is not set! "

        # check var_c
        if self.var_c is None:
            error += "C is not set! "
        
        # check output_format
        if len(self.output_format) == 0:
            error += "Output format not set! "
        
        # check sequence_type
        if len(self.sequence_type) < 1:
            error += "Sequence Type not set! "

        # check if any config values not set
        if len(error) > 1:
            return error
        else:
            return OK

    def set_config(self):
        "This method sets the self.seq_config variable - returns True if successful, False if unsuccessful"

        # check if config options set
        errorVal = self.check_config()
        if errorVal != OK:
            # call method to print error to screen
            # return error
            return False

        # all config options set, so fill self.seq_config
        self.seq_config['batDir'] = self.input_dir
        self.seq_config['A'] = self.var_a
        self.seq_config['B'] = self.var_b
        self.seq_config['C'] = self.var_c
        self.seq_config['outputContent'] = ""
        self.seq_config['roundingEnabled'] = self.rounding_enabled
        self.seq_config['P'] = 'Pause'
        self.seq_config['outputDirPath'] = ""
        self.seq_config['seqType'] = self.sequence_type
        self.seq_config['PauseDur'] = self.pause_duration

        return True

        

    def run_seqanalysis(self):
        "This method performs the sequence analysis on all .its files"
        
        # call setconfig
        r = self.set_config()

        test_config = {'batDir': '/home/syran/School/newLena/LENA_contingencies/its', 'A': 'FAF', 'C': '', 'outputContent': '', 'roundingEnabled': 'True', 'P': 'Pause', 'B': 'CXN', 'outputDirPath': '', 'seqType': 'A_B', 'PauseDur': '0.4'}
        test_batDir = '/home/syran/School/newLena/LENA_contingencies/its'

        # threading vars
        results = []
        tLock = threading.Lock()
        threads=[]

        # testing
        t = time.time()

        # run analysis on all found .its files
        for k,v in self.its_file_dict.items.iteritems():
            
            sa = SeqAnalysis(test_config, k, v)
            proc = threading.Thread(target=sa.Perform, args=(str(v[0]), results, tLock))
            threads.append(proc)
            proc.start()
            
        # wait for threads to finish
        for proc in threads:
            proc.join()
            print("thread done: "+proc.getName())

        # testing
        print("Time: "+str(time.time()-t))
        print(str(results))

        # output file
        if 'csv' in self.output_format:
            self.output_csv(results)
        if 'txt' in self.output_format:
            self.ouput_txt(results)
        if 'xlsx' in self.output_format:
            self.output_xlsx(results)
        
        # send success message to window


    def load_config(self):
        "This method loads a config file for the program"

    def reset_config(self):
        "This method resets the all program options"
    
    def save_config(self):
        "This method allows the user to save the program's current configuration"
    
    def load_instruction_window(self):
        "This method loads a separate window with program instructions"

    def ouput_txt(self, results):
        "This method outputs the analysis results to a .txt file"

    def output_csv(self, results):
        "This method outputs the analysis results to a .csv file"

    def output_xlsx(self, results):
        "This method outputs the analysis results to a .xlsx file"

    def set_config_from_file(self, config):
        "This method applies the config variable passed to it to the program"