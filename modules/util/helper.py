#!/usr/local/bin/python3


from os import path
from pathlib import Path
from jproperties import Properties
from csv import reader

import os.path
import requests
import csv
import logging
import sys



logger=logging.getLogger()

http_status_code = {
    200: 'ok',
    400: 'bad_request',
    404: 'not found',
    408: 'request timeout',
    500: 'Internal Server Error'
}

def get_url(account_id):
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get("REQUEST_URL").data.strip() + str(account_id).strip()


def is_csv_file(input_file, extension=".csv"):

    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(input_file)[-1].lower()
    return ext==extension

def get_data_from_api(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        logging.error('GET /tasks/ {}'.format(resp.status_code))
        raise Exception('GET /tasks/ {}'.format(resp.status_code))

def merge_data(input_data, api_response_data):
    
    if input_data and api_response_data:
        return csv_data(input_data['Account ID'], input_data['First Name'],input_data['Created On'], api_response_data['status'], api_response_data['created_on'] )

    return

def append_to_file(out_csv_file, result_set):
    print('append')
    with open(out_csv_file, mode='a+') as csv_file:
        fieldnames=["Account ID", "First Name", "Created On", "Status", "Status Set On"]
        writer = csv.DictWriter( csv_file, fieldnames = fieldnames)
        
        if csv_file.tell() == 0:
            writer.writeheader()
        
        for result in result_set:
            writer.writerow({"Account ID":result.account_id, "First Name":result.first_name, "Created On":result.created_on, "Status":result.status, "Status Set On":result.status_set_on})

def overwrite_file(out_csv_file, result_set):
     with open(out_csv_file, mode='w') as csv_file:
           
        fieldnames=["Account ID", "First Name", "Created On", "Status", "Status Set On"]
        writer = csv.DictWriter( csv_file, fieldnames = fieldnames)
        writer.writeheader()
        
        for result in result_set:
            writer.writerow({"Account ID":result.account_id, "First Name":result.first_name, "Created On":result.created_on, "Status":result.status, "Status Set On":result.status_set_on})

def get_accounts_data(input_csv_file):

    try:
        result_values = []
        if path.exists(input_csv_file):
            input_csv_file = Path(input_csv_file)
            
            with open(input_csv_file, 'r', encoding='utf-8-sig') as csvfile:

                d_reader = csv.DictReader(csvfile)

                # to takecare of redudant accounts, use set datatype
                distinct_accounts = set([])
                
                # get fieldnames from DictReader object and store in list
                headers = d_reader.fieldnames

                for row in d_reader:
                    
                    account_id = row[headers[0]]
                    if account_id and account_id not in distinct_accounts:
                        logger.info('getting data for account_id:  {}'.format(account_id))
                        distinct_accounts.add(account_id)
                        api_response_data = get_data_from_api(get_url(account_id))
                        logger.info('data for account_id {}: {}'.format(account_id, api_response_data))
                        result_values.append(merge_data(row,api_response_data))

        return result_values

    except Exception as e:
        raise Exception("Exception while retrieving the data: " + str(e))

# function to merge the data and save the file
def write_to_output_file(out_csv_file, result_set, append=False):

    # If append functionality is required, set append to true. 
    # by default output file will be overwritten
    if append:
        logger.info('appending data to the output file....')
        append_to_file(out_csv_file, result_set)
    
    # overwrite the file
    else:
        logger.info('writing data to the output file....')
        overwrite_file(out_csv_file, result_set)

class csv_data():
    def __init__(self,account_id, first_name='',created_on='', status='', status_set_on=''):
        self.account_id = account_id
        self.first_name = first_name
        self.created_on = created_on
        self.status = status
        self.status_set_on = status_set_on