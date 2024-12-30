# DogeFuzz's Benchmark

This project is a benchmark for [DogeFuzz](https://github.com/pamunb/dogefuzz) project.

## Running the benchmark using a configuration script and docker

To run a benchmark using a script, copy the script.json file:

```
cp script.json.template script.json
```

And execute the script:

```
benchmark.sh script <script_name>
```

## Running the benchmark using command line arguments and docker

To run all contracts available, run the following command passing the duration, type of fuzzing, repetition times, and prefix for the result folder:

```
benchmark.sh all <uri_or_folder> 30m directed_greybox 1 test1
```

Available options for the type of fuzzing are (to pass multiple types, use ';' as separator):

- blackbox
- greybox
- directed_greybox

Available options for duration are:

- 1m
- 5m
- 15m
- 30m
- 60m
  
## Running the project locally (without docker)
This project uses Python 3.10 and [Poetry](https://python-poetry.org/) to manage its dependencies and virtual environment.

To run the project using a script, execute the following commands:
```
cp script.json.template script.json
poetry run benchmark script <script_name>
```

To run the project with all available contracts, run the following command:

```
poetry run benchmark all <uri_or_folder> 30m directed_greybox
```
