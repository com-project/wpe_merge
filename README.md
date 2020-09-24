# wpe_merge

## About
 merge applications reads from the provided CSV file and combines its information
 with data from the API (http://interview.wpengine.io/v1/docs/) and outputs to a new CSV file.

## Pre-requirements
* `python 3.x.x`
* `curl`

# Steps to install pip
* download get-pip.py with curl `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
* Then run the following command in the folder where you have downloaded get-pip.py
* `python get-pip.py`

# Project dependencies 
* To install dependencies run
    * `pip install -r requirements.txt`

## Run the utility

### Mac
   * if python2 and python3 is installed on a machine, update the shell script with the following
   ```
      #!/bin/sh
      python3 merge.py $1 $2
   ```
   *  `chmod 0744 wpe_merge.sh`
   * `./wpe_merge.sh <input_file.csv> <output_file.csv>`
   * example : `./wpe_merge.sh tests/resource/input.csv output_file.csv`

### Windows
   * `wpe_merge.bat <input_file.csv> <output_file.csv>`
   * example :  `wpe_merge.bat test/resource/input_file.csv output_file.csv`

## logs
 * log file <wpe_merge.log> gets generated at the project level directory

## Unit tests
### Running tests

To run with a full coverage report:
  * `pip3 install coverage`
  * `coverage run --source=. -m unittest discover tests` which runs the tests and gathers coverage report data.
  * `coverage report -m` to view the coverage report.
