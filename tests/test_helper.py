#from unittest import TestCase
import unittest
import os
import csv
from csv import reader
from os import path
from pathlib import Path

import sys
sys.path.append('.')
from modules.util import helper

http_url = 'http://interview.wpengine.io/v1/accounts/'.strip()
ROOT_DIR = path.abspath(os.curdir)
resource_dir = path.join(ROOT_DIR,'tests', 'resource')
input_file = path.join(resource_dir, 'input.csv')
out_file = path.join(resource_dir, 'output.csv')

class TestUtils(unittest.TestCase):
    
    # test get url
    def test_get_url(self):
        expected_result = http_url+"123"
        # test with interger input
        acc_id = 123
        actual_result = helper.get_url(acc_id)
        self.assertEqual(actual_result, expected_result)

        # test with string input
        acc_id = "123"
        actual_result = helper.get_url(acc_id)
        self.assertEqual(actual_result, expected_result)

    def test_csv_extension(self):
        # postive test case
        actual_res = helper.is_csv_file(input_file)
        self.assertEqual(actual_res, True)

        # negative test case
        temp_input_file = path.join(resource_dir, 'input.txt')
        actual_res = helper.is_csv_file(temp_input_file)
        self.assertEqual(actual_res, False)
    

    def test_get_data_from_api(self):
    
        expected_result_dict = {'account_id': 12345, 'status': 'good', 'created_on': '2011-01-12'}
        actual_res = helper.get_data_from_api(http_url+"12345")
        self.assertEqual(actual_res, expected_result_dict)

        #print(helper.get_data_from_api(http_url+"123"))

    def test_negative_get_data_from_api(self):

        url = helper.get_url("0123xb")
        self.assertRaises(Exception, helper.get_data_from_api, url)

        # check with Null
        url = helper.get_url(None)
        self.assertRaises(Exception, helper.get_data_from_api, url)

    def test_merge_single_account_data(self):

        acc_id = '12345'
        input_data = None
        api_response_data = {'account_id': 12345, 'status': 'good', 'created_on': '2011-01-12'}
        with open(input_file, 'r', encoding='utf-8-sig') as csvfile:
            d_reader = csv.DictReader(csvfile)
            headers = d_reader.fieldnames

            for row in d_reader:
                if row[headers[0]] == acc_id:
                    input_data = row
                    break
        
        res_set = helper.merge_data(input_data, api_response_data)
        # check for status created on after merging with api repsonse data
        self.assertEqual(res_set.status_set_on, api_response_data['created_on'])

    def test_wpe_merge(self):

        expected_number_of_rows = 7
        expected_number_of_headers = 5

        actual_nunber_of_rows = 0
        result_set = helper.get_accounts_data(input_file)
        helper.write_to_output_file(out_file, result_set)
        self.assertTrue(path.exists(out_file))

        # count number of rows in the output file
        with open(out_file, 'r', encoding='utf-8-sig') as csvfile:
            d_reader = csv.DictReader(csvfile)
            actual_number_of_headers = len(d_reader.fieldnames)
            actual_nunber_of_rows = len(list(d_reader))
        
        # check for count of headers after merging the data with expected data
        self.assertEqual(actual_number_of_headers, expected_number_of_headers)

        # check for count of accounts after merging the data with expected data
        self.assertEqual(actual_nunber_of_rows, expected_number_of_rows)

        # delete outfile at the end of the test
        if os.path.exists(out_file):
            os.remove(out_file)