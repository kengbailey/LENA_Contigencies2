import csv
import xlsxwriter
import datetime

# Sequence Analysis Data Object
# Holds all items needed for analysis
class SeqData:
    its_dict = None
    seq_config = None
    num_threads = None
    output_format = None

    def __init__(self, its_dict, seq_config, num_threads, output_format):
        self.num_threads = num_threads
        self.its_dict = its_dict
        self.seq_config = seq_config
        self.output_format = output_format

# Sequence Analysis Run Object
# Put into queue; used in Perform()
class SeqRun:
    p_id = None
    path = None

    def __init__(self, p_id, path):
        self.p_id = p_id
        self.path = path

# Output Object
# sent to output functions
class OutData:
    batch_store = None
    seq_config = None
    results = None

    def __init__(self, batch_store, seq_config, results):
        self.batch_store = batch_store
        self.seq_config = seq_config
        self.results = results

# Output to CSV format
def output_csv(out_data):
    "This method outputs the analysis results to a .csv file"
    # output code
    print("Output in .csv")

    # create + write csv file
    out_file = out_data.seq_config['outputDirPath'] +'//'+ "LC2-"+out_data.batch_store+"-"+out_data.seq_config['seqType']+"-"+str(out_data.seq_config['PauseDur']).replace('.','p')+"-"+str(out_data.seq_config['roundingEnabled'])+"-"+datetime.datetime.now().strftime('%m%d%y-%H%M')+".csv"
    with open( out_file, 'wb') as f:#open csv file to be written in
        csv_writer = csv.writer(f, delimiter = ',')
        for line in out_data.results:#loop to write rows to csv file
            line = line.split(',')
            csv_writer.writerow(line)

# Output to TXT format
def ouput_txt(out_data):
    "This method outputs the analysis results to a .txt file"
    # output code 
    print("Output in .txt")

    # create + write txt file
    out_file = out_data.seq_config['outputDirPath'] +'//'+ "LC2-"+out_data.batch_store+"-"+out_data.seq_config['seqType']+"-"+str(out_data.seq_config['PauseDur']).replace('.','p')+"-"+str(out_data.seq_config['roundingEnabled'])+"-"+datetime.datetime.now().strftime('%m%d%y-%H%M')+".txt"
    with open(out_file,'w') as f:
        for line in out_data.results:
            f.writelines(line+"\n")

# Output to Excel format
def output_xlsx(out_data):
    "This method outputs the analysis results to a .xlsx file"
    print("Output in .xlsx")
    # create workbook & add sheet
    out_file = out_data.seq_config['outputDirPath'] +'//'+ "LC2-"+out_data.batch_store+"-"+out_data.seq_config['seqType']+"-"+str(out_data.seq_config['PauseDur']).replace('.','p')+"-"+str(out_data.seq_config['roundingEnabled'])+"-"+datetime.datetime.now().strftime('%m%d%y-%H%M')+".xlsx"
    workbook = xlsxwriter.Workbook(out_file)
    worksheet = workbook.add_worksheet()

    # start from first cell
    row = 0
    
    # insert into worksheet
    for line in out_data.results:
        col = 0
        for cell in str(line).split(","):
            worksheet.write(row, col, cell)
            col += 1
        row += 1

    # close file
    workbook.close()