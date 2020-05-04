# Hydro Generator Presentation
## Summary
This code is meant to accompany the technical presentation on Hydro Generators. 

## Test Version: MVP
`pytest --junitxml="result.xml" --testver=0 --testround=1`
`pytest --junitxml="result.xml" --testver=0 --testround=2`


## How to use this code
Install all dependencies using the requirements file. It is highly recommended to do this in a Python3 virtual environment.
Run `pytest` by specifying `testver` and `testround`. This will create a new set of results for 100 Hydro Generators, for the specified test version and testing round.
You can see a graphical representation of results by running `python plotresults.py`, which will graph all errors found for each device.

