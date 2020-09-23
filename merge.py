#!/usr/local/bin/python3

"""
Usage:
    python3 merge.py <input_file> <output_file>
"""
import sys
import csv
import logging
from pathlib import Path
from os import path
from modules.util import helper


levels = {
'debug': logging.DEBUG,
'info': logging.INFO,
'warning': logging.WARNING
}
log_format="%(asctime)s %(levelname)s %(message)s" 
log_filename= 'wpe_merge.log'

logging.basicConfig(filename=log_filename,
                    level=levels['warning'],
                    format=log_format, 
                    filemode='w'
                    )

logger=logging.getLogger()
logger.info('Logger initialized')

def validate_inputs_params(input_file, out_file):
        # check for input file
    if not path.exists(input_file):
        sys.exit('input file {} does not exists'.format(input_file))
    
    # check for output parent directory
    if not path.exists(Path(out_file).parent):
         sys.exit('parent directory {} for output file {} does not exists'.format(Path(out_file).parent, out_file))
    
    # check for file extension
    if not helper.is_csv_file(input_file):
        sys.exit('invalid input file extension')

    # check for file extension
    if not helper.is_csv_file(out_file):
        sys.exit('invalid output file extension')

def usage():
    usage = "Usage: \n python3 merge.py <input_file> <output_file>"
    sys.exit(usage)

def main():

    args_len = len(sys.argv[1:])

    if (args_len < 1): 
        usage()

    if (args_len < 2): 
        usage()

    input_file = sys.argv[1]
    out_file = sys.argv[2]
    
    # validate inputs
    validate_inputs_params(input_file, out_file)
    
    # result set from merging the input account's data and API account's data
    logger.info('read accounts data...')
    result_set = helper.get_accounts_data(input_file)

    # write to the given output file
    helper.write_to_output_file(out_file, result_set)
    print('merged the data!!!')

# ----------------------------------------------------------------
# Main
# -----------------------------------------------------------------
if __name__ == "__main__":
    
    main()
    
