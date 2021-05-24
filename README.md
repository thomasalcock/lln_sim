# LLN Simulator
A Python Streamlit application to simulate the behaviour of standard summary statistics with growing sample sizes.
Users can choose one of the following distributions:
- Gaussian
- Lognormal
- Pareto

and speficy the appropriate parameters, as well as the maximum and minimum sample sizes.
Once specified, one or more sample statistics can be selected to simulate:

- mean
- standard deviation
- skewness 
- kurtosis (Fisher's definition)

## Running the App
- `make build` builds the application on top of python:3.9.5-slim-buster
- `make run` runs the app on port 8501

## Depenedencies
Managed with `pip` and `venv`. Activate the virtualenvironment using `source ./venv/bin/activate`,
install dependencies with pip and use `pip freeze > requirements.txt` to update the package list.