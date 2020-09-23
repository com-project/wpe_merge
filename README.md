# wpe_merge
## Usage
* chmod 0744 wpe_merge.sh
* ./wpe_merge.sh /Users/gitRepo/wpe_merge/input_file.csv /Users/gitRepo/wpe_merge/output_file.csv 

## Requirements
* `python 3.7.x`

# Steps to install pip
* download get-pip.py with curl `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
* Then run the following command in the folder where you have downloaded get-pip.py
* `python get-pip.py`

# project dependencies 
* To install dependencies run
    * `pip install -r requirements.txt`

## Unit tests
### Running tests

To run with a full coverage report:
  * `pip3 install coverage`
  * `coverage run --source=. -m unittest discover tests` which runs the tests and gathers coverage report data.
  * `coverage report -m` to view the coverage report.
