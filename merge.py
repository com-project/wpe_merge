#!/usr/local/bin/python3

"""
 This code reads from the provided CSV file and
 combines its information with data from the API (http://interview.wpengine.io/v1/docs/)
 and outputs a new CSV file.
"""

"""
Usage:
    python3 merge.py <input_file> <output_file>
"""

import sys
import logging
import traceback

from pathlib import Path
from os import path
from modules.util import helper

# log levels
levels = {
'debug': logging.DEBUG,
'info': logging.INFO,
'warning': logging.WARNING,
'error': logging.ERROR
}
log_format="%(asctime)s %(levelname)s %(message)s" 
log_filename= 'wpe_merge.log'

logging.basicConfig(filename=log_filename,
                    level=levels['debug'],
                    format=log_format, 
                    filemode='w'
                    )

logger=logging.getLogger()
logger.info('Logger initialized')

def validate_inputs_params(input_file, out_file):
    """
    checks if files exits and have correct extensions
    """
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
    """
    prints usage
    """
    usage = "Usage: \n python3 merge.py <input_file> <output_file>"
    sys.exit(usage)

def main():
    """
    main method
    """
    try:
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
        if result_set:
            helper.write_to_output_file(out_file, result_set)
            print('merged the data!!!')
        else:
            print('empty input file, nothing to merge.')
    except Exception as ex:
        print('Failed to merge the data')
        logger.error("Failed to merge the data...")
        logger.error(str(ex),exc_info=True)
# ----------------------------------------------------------------
# Main
# -----------------------------------------------------------------
if __name__ == "__main__":
    
    main()
    
