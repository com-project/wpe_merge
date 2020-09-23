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


class TestMerge(unittest.TestCase):
    
    def test_validate_inputs_params(self):
        print('1')

    def test_negative_validate_inputs_params(self):
        print('1')
    
    
    