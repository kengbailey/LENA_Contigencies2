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
import xlsxwriter
import ast
import csv
import tkMessageBox

MAC = 'Darwin'
AB = 'A_B'
ABC = 'AB_C'
OK = 'ok'
MAXTHREADS = 4
codes = ('MAN','MAF','FAN','FAF','CHNSP','CHNNSP', \
			'CHF','CXN','CXF','NON','NOF','OLN','OLF','TVN', \
			'TVF','SIL')

class LenaUI:

    "This class is the UI and associated actions"
    def __init__(self, root):
        "UI started on init of class"        
        self.root = root
        root.resizable(False, False)
        root.title("LENA Contingencies")

        # Class Attributes
        self.its_file_dict = {} # k:ID v:path/to/file
        self.input_dir = StringVar()
        self.output_dir = StringVar()
        self.output_format = []
        self.seq_config = {}
        self.pause_duration = DoubleVar()
        self.pause_duration.set(0.1)
        self.rounding_enabled = BooleanVar()
        self.sequence_type = StringVar()
        self.var_a = []
        self.var_b = []
        self.var_c = []
        self.output_format.append(".csv") # set to csv default
        self.output_msg = ""
        self.output_msg_counter = 0
        self.num_threads = IntVar()
        self.num_threads.set(4)
        

        # Create main frames
        main_frame = ttk.Frame(self.root) # top, mid, btm frames embedded within this frame
        self.top_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=150)
        self.mid_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=300)
        self.btm_frame = ttk.Frame(main_frame, borderwidth=5, relief="sunken", width=300, height=100)

        # create menu
        menubar = Menu(root) # create menu bar
        root.config(menu=menubar) # attach menubar to root window

        # file menu
        file_menu = Menu(menubar) # create "File" menu item 
        file_menu.add_command(label="Exit", command=self.close_program) # add a command to "File" menu item
        menubar.add_cascade(label="File", menu=file_menu)   # attach "File" menu item to menubar
        
        # help menu
        help_menu = Menu(menubar) # create "Help" menu item 
        help_menu.add_command(label="Instructions", command=self.load_instruction_window) # add a command to "Help" menu item
        help_menu.add_command(label="Thread Count", command=self.new_threads_window)
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

    def new_threads_window(self):
        # setup
        t = Toplevel(self.root)
        t.resizable(False, False)

        # create widgets
        top_frame = Frame(t, width=100, height=50)
        t.wm_title("Set Threads")
        l = Label(t, text="Set number of threads to use\nwhen performing analysis: \n(default=4)")
        s = Spinbox(t, from_=4, to=50, textvariable=self.num_threads, width=4)
        b = ttk.Button(t, text="close", command=lambda: t.destroy(), width=4)

        # arrange widgets
        l.grid(row=0, column=0, padx=5, pady=7)
        s.grid(row=1, column=0, sticky=W, padx=15, pady=5)
        b.grid(row=1,column=0, sticky=E, padx=15, pady=5)

    def change_pause_legnthU(self, event):
        if self.pause_duration.get() < 10.0:
            self.pause_duration.set(round(self.pause_duration.get()+0.1,1))

    def change_pause_lengthD(self, event):
        if self.pause_duration.get() >= 0.1:
            self.pause_duration.set(round(self.pause_duration.get()-0.1,1))

    def rounding_pause_length(self,event):
        self.pause_duration.set(round(self.pause_duration.get(),1))

    def setup_top_frame(self):
        # TOP FRAME CONFIG
        # Create top frame widgets
        self.csv_var = BooleanVar() # holds user selection for csv output
        self.txt_var = BooleanVar() # holds user selection for txt output
        self.xl_var = BooleanVar()  # holds user selection for xlsx output

        top_dir_label = ttk.Label(self.top_frame, text="Specify Directory")
        top_reset_btn = ttk.Button(self.top_frame, text="RESET", command=self.reset_config)
        top_load_btn = ttk.Button(self.top_frame, text="LOAD", command=self.save_config)
        top_save_btn = ttk.Button(self.top_frame, text="SAVE", command=self.save_config)
        top_input_label = ttk.Label(self.top_frame, text="Input:")
        top_output_label = ttk.Label(self.top_frame, text="Output:")
        top_format_label = ttk.Label(self.top_frame, text="Output Format")        
        self.top_csv_btn = ttk.Checkbutton(self.top_frame, text='.csv', command=self.set_output_var, variable=self.csv_var,onvalue=1, offvalue=0)
        self.csv_var.set(1) # set to csv default
        self.top_txt_btn = ttk.Checkbutton(self.top_frame, text=".txt", command=self.set_output_var, variable=self.txt_var,onvalue=1, offvalue=0)
        self.top_xl_btn = ttk.Checkbutton(self.top_frame, text=".xlsx", command=self.set_output_var, variable=self.xl_var,onvalue=1, offvalue=0)
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
        self.top_csv_btn.grid(row=6, column=0)
        self.top_txt_btn.grid(row=6, column=1)
        self.top_xl_btn.grid(row=6, column=2)
        top_load_btn.grid(row=0, column=2)
        top_save_btn.grid(row=0, column=1)

    def update_var(self, event):

        # get user selection; id -> value
        selection = event.widget.curselection()
        templist = []
        for sel in selection:
            templist.append(event.widget.get(sel))

        # assign to appropriate var_
        if (event.widget == self.mid_abc_a_box):
            self.var_a = templist
            print("A: "+str(self.var_a))
        elif (event.widget == self.mid_abc_b_box):
            self.var_b = templist
            print("B: "+str(self.var_b))
        elif (event.widget == self.mid_abc_c_box):
            self.var_c = templist
            print("C: "+str(self.var_c))

    def setup_mid_frame(self):
        # MID FRAME CONFIG
        # create mid frame widgets
        code_vars = StringVar(value=codes)

        self.mid_abc_a_box = Listbox(self.mid_frame, height=16, listvariable=code_vars, selectmode=MULTIPLE, width=9, exportselection=False)
        self.mid_abc_b_box = Listbox(self.mid_frame, height=16, listvariable=code_vars, selectmode=MULTIPLE, width=9, exportselection=False)
        self.mid_abc_c_box = Listbox(self.mid_frame, height=16, listvariable=code_vars, selectmode=MULTIPLE, width=9, exportselection=False)
        
        self.mid_abc_a_box.bind("<<ListboxSelect>>", self.update_var)
        self.mid_abc_b_box.bind("<<ListboxSelect>>", self.update_var)
        self.mid_abc_c_box.bind("<<ListboxSelect>>", self.update_var)

        def disable_c():
            self.mid_abc_c_box.configure(state="disable")
            self.mid_abc_c_box.update()

        def enable_c():
            self.mid_abc_c_box.configure(state="normal")
            self.mid_abc_c_box.update()

        mid_type_label = ttk.Label(self.mid_frame, text='Type of Analysis')       
        self.mid_ab_btn = ttk.Radiobutton(self.mid_frame, text='A ---> B', variable=self.sequence_type, value=AB, command=disable_c)
        self.mid_abc_btn = ttk.Radiobutton(self.mid_frame, text='( A ---> B ) ---> C', variable=self.sequence_type, value=ABC, command=enable_c)        
        mid_filler_label = ttk.Label(self.mid_frame, text="     ")
        mid_conf_label = ttk.Label(self.mid_frame, text="Configure Analysis")
        mid_conf_abc_a_label = ttk.Label(self.mid_frame, text="A") 
        mid_conf_abc_b_label = ttk.Label(self.mid_frame, text="B") 
        mid_conf_abc_c_label = ttk.Label(self.mid_frame, text="C") 
 
        mid_filler_label2 = ttk.Label(self.mid_frame, text="     ")
        mid_pause_label = ttk.Label(self.mid_frame, text="Pause Duration")
        mid_filler_label3 = ttk.Label(self.mid_frame, text="     ")
        self.mid_pause_slider = ttk.Scale(self.mid_frame, orient=HORIZONTAL, length=100, from_=0.0, to=10.0, variable=self.pause_duration,command=lambda r: self.rounding_pause_length(self))
        mid_pause_dn_btn = ttk.Button(self.mid_frame, text="<", command=lambda: self.change_pause_lengthD(self), width=1)
        mid_pause_up_btn = ttk.Button(self.mid_frame, text=">", command=lambda: self.change_pause_legnthU(self), width=1)
        self.mid_pause_entry = ttk.Entry(self.mid_frame, textvariable=self.pause_duration, width=4)
        self.mid_pause_checkbox = ttk.Checkbutton(self.mid_frame, text="Enable rounding", variable=self.rounding_enabled,onvalue=True, offvalue=False)


        # setup mid frame widgets
        mid_type_label.grid(row=0, column=0, columnspan=4)
        self.mid_ab_btn.grid(row=1, column=0, columnspan=3, sticky = W)
        self.mid_abc_btn.grid(row=2, column=0, columnspan=3, sticky = W)
        mid_conf_abc_a_label.grid(row=3, column=0)
        mid_conf_abc_b_label.grid(row=3, column=1)
        mid_conf_abc_c_label.grid(row=3, column=2)
        self.mid_abc_a_box.grid(row=4, column=0)
        self.mid_abc_b_box.grid(row=4, column=1)
        self.mid_abc_c_box.grid(row=4, column=2)

        mid_filler_label3.grid(row=5, column=0, columnspan=3)
        mid_pause_label.grid(row=6, column=0, columnspan=4, pady=5)
        self.mid_pause_entry.grid(row=7, column=0)
        self.mid_pause_slider.grid(row=7, column=1, sticky=W)
        mid_pause_dn_btn.grid(row=7, column=2, sticky=E)
        mid_pause_up_btn.grid(row=7, column=3, sticky=W)
        self.mid_pause_checkbox.grid(row=8, column=0, pady=4, columnspan=4)

    def setup_btm_frame(self):
        # BOTTOM FRAME CONFIG
        # create bottom frame widgets

        btm_submit_btn = ttk.Button(self.btm_frame, text="Submit", command=self.run_seqanalysis)
        self.btm_progress_bar = ttk.Progressbar(self.btm_frame, orient=HORIZONTAL, length=200, mode='determinate')
        self.btm_text_window = Text(self.btm_frame, width=45, height=5)
        self.btm_text_window.config(state=DISABLED)

        # arrange bottom frame widgets
        btm_submit_btn.grid(row=0, column=1)
        self.btm_progress_bar.grid(row=0, column=0)
        self.btm_text_window.grid(row=1, column=0, columnspan=2)

    def select_input_dir(self):
        self.input_dir.set(tkFileDialog.askdirectory())

    def select_output_dir(self):
        self.output_dir.set(tkFileDialog.askdirectory())

    def get_its_files(self):
        "This method looks creates a dict of all .its files found in the input directory"
        self.its_file_dict = Batch(self.input_dir.get())

    def check_config(self):
        "This method checks if all seq_config values are set. Returns error message if any aren't set."

        # check input directory
        if len(str(self.top_in_path.get())) < 2:
            return "Input directory not set! "

        # check output directory
        if len(str(self.top_out_path.get())) < 2:
            return "Output directory not set! "

        # check sequence_type
        if str(self.sequence_type.get()) not in (AB, ABC):
            return "Sequence Type not set! "

        # check var_a
        if not self.var_a:
            return "A is not set! "

        # check var_b
        if not self.var_b:
            return "B is not set! "

        # check var_c
        if (self.sequence_type.get() == ABC):
            if not self.var_c:
                return "C is not set! "

        # check output_format
        if not self.output_format:
            return "Output format not set! "
        else:
            self.write_to_window("All config options are valid!")
        
        return OK

    def set_config(self):
        "This method sets the self.seq_config variable - returns True if successful, False if unsuccessful"

        # check if config options set
        errorVal = self.check_config()
        if errorVal != OK:
            self.write_to_window(errorVal)
            return False

        # all config options set, so fill self.seq_config
        self.seq_config['batDir'] = self.top_in_path.get()
        self.seq_config['A'] = ','.join(map(str, self.var_a)) 
        self.seq_config['B'] = ','.join(map(str, self.var_b))
        self.seq_config['C'] = ','.join(map(str, self.var_c))
        self.seq_config['outputContent'] = ""
        self.seq_config['roundingEnabled'] = str(self.rounding_enabled.get())
        self.seq_config['P'] = 'Pause'
        self.seq_config['outputDirPath'] = self.top_out_path.get()
        self.seq_config['seqType'] = self.sequence_type.get()
        self.seq_config['PauseDur'] = str(round(self.pause_duration.get(), 1))

        self.write_to_window("Config options assembled!")
        return True

    def run_seqanalysis(self):
        "This method performs the sequence analysis on all .its files"
        
        # check config
        r = self.set_config()
        if r != True:
            return 
        
        # start analysis 
        thread = threading.Thread(target=self.sequence_analysis)
        thread.start()

    def sequence_analysis(self):
        # disable window
        self.write_to_window("Performing analysis!")
        self.disable_widgets()
            
        # threading vars
        results = []
        tLock = threading.Lock()
        self.get_its_files()
        t = time.time()

        # progress bar setup
        progress = 30
        self.btm_progress_bar['value']=progress
        self.btm_progress_bar['maximum']=200
        item_count = len(self.its_file_dict.items)
        print(item_count)
        incr = int(200 / item_count)
        print(incr)

        # run sequence analysis on MAXTHREADS at a time
        while len(self.its_file_dict.items) > 0:

            # grab its file to process in this batch
            tempDict = {}
            threads=[]
            for i in range(self.num_threads.get()): # num_threads implementation
                try:
                    tempItem = self.its_file_dict.items.popitem()
                    tempDict.update({tempItem[0]:tempItem[1][0]})
                except KeyError:
                    pass # dictionary is empty
            
            # run analysis on all batch .its files       
            for k,v in tempDict.iteritems():
                sa = SeqAnalysis(self.seq_config, k, v)
                proc = threading.Thread(target=sa.Perform, args=(str(v), results, tLock,))
                threads.append(proc)
                proc.start()
                
            # wait for threads to finish
            for proc in threads:
                proc.join()
                progress = progress + incr
                if progress > 200: progress = 200
                self.btm_progress_bar['value'] = progress
                print("thread done: "+proc.getName())
            done = time.time()-t
        
        # output file in parallel
        threads = []
        csv_proc = threading.Thread(target=self.output_csv, args=(results,))
        txt_proc = threading.Thread(target=self.ouput_txt, args=(results,))
        xl_proc = threading.Thread(target=self.output_xlsx, args=(results,))
        threads.extend([csv_proc, txt_proc, xl_proc])
        for proc in threads:
            proc.start()
        for proc in threads:
            proc.join()
        
        # send success message to window
        self.write_to_window("Successfully Sequence Analysis! Files processed in {} seconds".format(round(done, 2)))
        self.enable_widgets()
         
    def load_config(self):
        "This method loads a config file for the program"
        config_load_file = tkFileDialog.askopenfilename(initialdir="/", title="Select config file", filetypes=(("leco files", "*.leco"), ("all files", "*.*")))
        while not config_load_file.endswith('.leco'):
             config_load_file = tkFileDialog.askopenfilename(initialdir="/", title="Select config file (.leco)", filetypes=(("leco files", "*.leco"), ("all files", "*.*")))
        with open(config_load_file, 'r') as config_opened_file:
            config_info = config_opened_file.read()
            config_info = ast.literal_eval(config_info)
            assert type(config_info) is dict
            self.top_in_path = config_info['batDir']
            self.var_a = config_info['A']
            self.var_b = config_info['B']
            self.var_c = config_info['C']
            self.rounding_enabled = config_info['roundingEnabled']
            self.top_out_path = config_info['outputDirPath']
            self.sequence_type = config_info['seqType']
            self.pause_duration = config_info['PauseDur']
            config_opened_file.close()
        self.set_config()
        
    def reset_config(self):
        "This method resets the all program options"
        # re-initialize key variables used in the UI
        self.input_dir = StringVar()
        self.output_dir = StringVar()
        self.sequence_type = StringVar()
        self.pause_duration = DoubleVar()
        self.pause_duration.set(0.1)

        # re-initialize the A, B, & C entry boxes
        self.mid_abc_a_box.select_clear(0,END)
        self.mid_abc_b_box.select_clear(0,END)
        self.mid_abc_c_box.select_clear(0,END)
        self.var_a = []
        self.var_b = []
        self.var_c = []

        # re-initialize the selections
        self.output_format = []
        self.output_format.append(".csv")
        self.csv_var.set(1)
        self.txt_var.set(0)
        self.xl_var.set(0)
        self.rounding_enabled.set(0)

        # re-initialize the selections update
        self.top_csv_btn.configure(variable=self.csv_var)
        self.top_txt_btn.configure(variable=self.txt_var)
        self.top_xl_btn.configure(variable=self.xl_var)
        self.mid_pause_checkbox.configure(variable=self.rounding_enabled)
        self.top_csv_btn.update()
        self.top_txt_btn.update()
        self.top_xl_btn.update()
        self.mid_pause_checkbox.update()
    
        # reset the in and out dir update
        self.top_in_path.configure(textvariable=self.input_dir)
        self.top_out_path.configure(textvariable=self.output_dir)
        self.top_in_path.update()
        self.top_out_path.update()

        # reset the selection to nothing selected update
        self.mid_ab_btn.configure(variable=self.sequence_type)
        self.mid_abc_btn.configure(variable=self.sequence_type)
        self.mid_ab_btn.update()
        self.mid_abc_btn.update()

        # reset slider and pause_duration entry box update
        self.mid_pause_slider.configure(variable=self.pause_duration)
        self.mid_pause_entry.configure(textvariable=self.pause_duration)
        self.mid_pause_slider.update()
        self.mid_pause_entry.update()
        
    def save_config(self):
        "This method allows the user to save the program's current configuration"
        if self.check_config() == OK:
            self.set_config()
            config_save_file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".leco")
            seq_config_string = str(self.seq_config)
            config_save_file.write(seq_config_string)
            self.write_to_window("Configuration successfully saved! ")
            
    def load_instruction_window(self):
        "This method loads a separate window with program instructions"
        instruction_var = self.list_instructions() 
        tkMessageBox.showinfo("Instructions",self.list_instructions())
    
    def ouput_txt(self, results):
        "This method outputs the analysis results to a .txt file"
        if '.txt' in self.output_format:
            # output code 
            print("Output in .txt")
            out_file = self.seq_config['outputDirPath'] +'//'+ 'test.txt'
            with open(out_file,'w') as f:
                for line in results:
                    f.writelines(line+"\n")

    def output_csv(self, results):
        "This method outputs the analysis results to a .csv file"
        if '.csv' in self.output_format:
            # output code
            print("Output in .csv")
            out_file = self.seq_config['outputDirPath'] +'//'+ 'test.csv'
            with open( out_file, 'wb') as f:#open csv file to be written in
                csv_writer = csv.writer(f, delimiter = ',')
                for line in results:#loop to write rows to csv file
                    line = line.split(',')
                    csv_writer.writerow(line)

    def output_xlsx(self, results):
        "This method outputs the analysis results to a .xlsx file"
        if '.xlsx' in self.output_format:
            print("Output in .xlsx")
            # create workbook & add sheet
            out_file = self.seq_config['outputDirPath'] +'//'+ 'test.xlsx'
            workbook = xlsxwriter.Workbook(out_file)
            worksheet = workbook.add_worksheet()

            # start from first cell
            row = 0
            
            # insert into worksheet
            for line in results:
                col = 0
                for cell in str(line).split(","):
                    worksheet.write(row, col, cell)
                    col += 1
                row += 1

            # close file
            workbook.close()

    def reset_all_widgets(self):
        "This method resets all widgets"

    def close_program(self):
        "This method closes the program"
        self.root.quit()
    
    def write_to_window(self, message):
        "This method writes text to message box"

        # edit message text
        self.output_msg_counter += 1
        message = str(self.output_msg_counter)+": "+message +'\n'
        self.output_msg = message + self.output_msg

        # insert text
        # we must enable window to edit contents
        self.btm_text_window.config(state=NORMAL)
        self.btm_text_window.delete(1.0,END)
        self.btm_text_window.insert(END, self.output_msg)
        self.btm_text_window.config(state=DISABLED)

    def set_output_var(self):
        "This method sets the output var based on the user's selection"

        if self.csv_var.get() == 1:
            if ".csv" not in self.output_format:
                self.output_format.append(".csv")
        elif self.csv_var.get() == 0:
            if ".csv" in self.output_format:
                self.output_format.remove(".csv")

        if self.xl_var.get() == 1:
            if ".xlsx" not in self.output_format:
                self.output_format.append(".xlsx")
        elif self.xl_var.get() == 0:
            if ".xlsx" in self.output_format:
                self.output_format.remove(".xlsx")
        
        if self.txt_var.get() == 1:
            if ".txt" not in self.output_format:
                self.output_format.append(".txt")
        elif self.txt_var.get() == 0:
            if ".txt" in self.output_format:
                self.output_format.remove(".txt")
    
    def disable_widgets(self):
        "This method disables top and mid widgets"
        for child in self.top_frame.winfo_children():
            try:
                child.configure(state=DISABLED)
            except:
                pass
        for child in self.mid_frame.winfo_children():
            try:
                child.configure(state=DISABLED)
            except:
                pass

    def enable_widgets(self):
        "This method enables top and mid widgets"
        for child in self.top_frame.winfo_children():
            try:
                child.configure(state='enable')
            except:
                pass
        for child in self.mid_frame.winfo_children():
            try:
                child.configure(state='enable')
            except:
                pass
        
        # Listbox reset
        self.mid_abc_a_box.configure(state="normal")
        self.mid_abc_a_box.update()
        self.mid_abc_b_box.configure(state="normal")
        self.mid_abc_b_box.update()
        self.mid_abc_c_box.configure(state="normal")
        self.mid_abc_c_box.update()
    
    def list_instructions(self):
        instruction_var = "1) SAVE:  Saves all the data currently in all fields.\n"
        instruction_var += "2) LOAD:  Loads the data last saved in all fields.\n"
        instruction_var += "3) RESET:  Empties all fields\n"
        instruction_var += "4) Input:  Browse to the directory that contains all files for analysis.\n"
        instruction_var += "5) Output:  Browse to the desired directory for the output file."
        instruction_var += "4) INPUT:  Browse to the directory that contains all files for analysis\n"
        instruction_var += "5) OUTPUT:  Browse to the desired directory for the output file\n"
        instruction_var += "6) OUTPUT FORMAT:  Select the desired format for output file\n"
        instruction_var += "7) TYPE OF ANALYSIS:  Choose the type of analysis to be done and its variables\n"
        instruction_var += "\tA--->B  or  (A---> B)---> C: type of analysis performed\n"
        instruction_var += "\tA, B, C:  Drop down menus to select desired variables\n\n"
        instruction_var += "8) PAUSE DURATION:  Use entry field, slider bar, and/or buttons to choose pause duration\n"
        instruction_var += "\tEntry field:  enter in specific pause duration\n"
        instruction_var += "\tSlider bar:  Click and hold to move along bar\n"
        instruction_var += "\tButtons(<,>):  Moves slider bar by .1 in specified direction\n\n"
        instruction_var += "9) ENABLE ROUNDING:  Select to enable rouding\n"
        instruction_var += "10) SUBMIT:  Submits the current data in fields to the program to start analysis\n"
        return instruction_var