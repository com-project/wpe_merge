# wpe_merge

## prerequirements
* `python 3.7.x`
* `curl`

# Steps to install pip
* download get-pip.py with curl `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
* Then run the following command in the folder where you have downloaded get-pip.py
* `python get-pip.py`

# project dependencies 
* To install dependencies run
    * `pip install -r requirements.txt`

## run the utility

# mac
* `chmod 0744 wpe_merge.sh`
* `./wpe_merge.sh <input_file.csv> <output_file.csv>`
* example :
* `./wpe_merge.sh tests/resource/input.csv output_file.csv`

# windows
* `wpe_merge.bat <input_file.csv> <output_file.csv>`
* example :
* `wpe_merge.bat test/resource/input_file.csv output_file.csv`

* log file <wpe_merge.log> gets generated at the project level directory

## Unit tests
### Running tests

To run with a full coverage report:
  * `pip3 install coverage`
  * `coverage run --source=. -m unittest discover tests` which runs the tests and gathers coverage report data.
  * `coverage report -m` to view the coverage report.
