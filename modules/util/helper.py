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



def get_endpoint_url(account_id):
    """returns the API endpoint by concatenating the base url and account_id
    
    Parameters:
    account_id (string)

    returns:
    string: endpoint url

    """
    request_url=''
    
    if account_id:
        configs = Properties() 
        with open('app-config.properties', 'rb') as config_file:
            configs.load(config_file)
            request_url = configs.get("REQUEST_URL").data.strip()
            
            # check for API url
            if request_url:
                return request_url + str(account_id).strip()
            else:
                raise ValueError ("Endpoint url cannot be None")
    else:
        raise ValueError ("account id cannot be None")


def is_csv_file(input_file, extension=".csv"):
    """checks for a file extension. By default it checks for csv extension
    
    Parameters:
    input_file: name or absolute path of a file
    extension (string): extension of a file

    returns:
    boolean: True or False
    
    """

    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(input_file)[-1].lower()
    return ext==extension


def get_data_from_api(url):
    """return data from the requested url

    Parameters:
    url: API endpoint
    
    returns:
    json object

    """
    
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise Exception('GET task {} returned with status code {}'.format(url, resp.status_code))

def merge_data(input_data, api_response_data):
    """returns the merged data for an account
    from the given input and api reponse

    Parameters:
    input_data: data from the input file
    api_response_data: data from the api response object 
    
    returns:
    csv_data object

    """
    
    if input_data and api_response_data:
        logger.info('merged data for account_id {}: {}'.format(input_data['Account ID'],[ ('First Name',input_data['First Name']),('Created On',input_data['Created On']), ('status',api_response_data['status']), ('status_set_on', api_response_data['created_on'])]))
        
        return csv_data(input_data['Account ID'], input_data['First Name'],input_data['Created On'], api_response_data['status'], api_response_data['created_on'] )

    return


def overwrite_file(out_csv_file, result_set):
    """overwrites to the output file with the given 
    result set.

    Parameters:
    out_csv_file: output csv file
    result_set: result set of all acounts

    """
    with open(out_csv_file, mode='w') as csv_file:
        fieldnames=["Account ID", "First Name", "Created On", "Status", "Status Set On"]
        writer = csv.DictWriter( csv_file, fieldnames = fieldnames)
        writer.writeheader()
        
        for result in result_set:
            writer.writerow({"Account ID":result.account_id, "First Name":result.first_name, "Created On":result.created_on, "Status":result.status, "Status Set On":result.status_set_on})

# this method can be used if required

def append_to_file(out_csv_file, result_set):
    """appends to the output file with the given 
    result set.

    Parameters:
    out_csv_file: output csv file
    result_set: result set of all acounts

    """
    with open(out_csv_file, mode='a+') as csv_file:
        fieldnames=["Account ID", "First Name", "Created On", "Status", "Status Set On"]
        writer = csv.DictWriter( csv_file, fieldnames = fieldnames)
        
        if csv_file.tell() == 0:
            writer.writeheader()
        
        for result in result_set:
            writer.writerow({"Account ID":result.account_id, "First Name":result.first_name, "Created On":result.created_on, "Status":result.status, "Status Set On":result.status_set_on})

def get_accounts_data(input_csv_file):
    """returns the result set for the given input data

    Parameters:
    input_csv_file: file to read the account data
    
    returns:
    list of merged data in the form csv objects

    """
    result_values = []
    if path.exists(input_csv_file):
        input_csv_file = Path(input_csv_file)
        
        with open(input_csv_file, 'r', encoding='utf-8-sig') as csvfile:

            d_reader = csv.DictReader(csvfile)
            
            # convert DictReader to list for dictionaries
            accounts_list = list(d_reader)
            
            # if empty csv file, return 
            if  len(accounts_list) == 0:
                logger.info('empty input file')
                return

            # takes care of redudant accounts
            distinct_accounts = set([])
            # get fieldnames from DictReader object and store in list
            headers = d_reader.fieldnames

            for row in accounts_list:

                account_id = row['Account ID']
                if account_id and account_id not in distinct_accounts:
                    logger.info('getting data for account_id:  {}'.format(account_id))
                    distinct_accounts.add(account_id)

                    # get endpoint url
                    endpoint_url = get_endpoint_url(account_id)
                    api_response_data = get_data_from_api(endpoint_url)
                    logger.info('Api data for account_id {}: {}'.format(account_id, api_response_data))
                    result_values.append(merge_data(row,api_response_data))

        return result_values

# function to merge the data and save the file
def write_to_output_file(out_csv_file, result_set, append=False):

    """
    if append is set to false, overwrite the file

    Parameters:
    out_csv_file: output file
    result_set: list of CSV objects
    append: by default the value is False
    """

    logger.info('writing data to the output file....')
    overwrite_file(out_csv_file, result_set)
    logger.info('Done writing to the output file!!')

#### csv_data class ###
class csv_data():
    """
    account structure for merged data
    """
    def __init__(self,account_id, first_name='',created_on='', status='', status_set_on=''):
        self.account_id = account_id
        self.first_name = first_name
        self.created_on = created_on
        self.status = status
        self.status_set_on = status_set_on