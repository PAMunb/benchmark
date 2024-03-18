# DogeFuzz's Benchmark

This project is a benchmark for [DogeFuzz](https://github.com/pamunb/dogefuzz) project.

## Running the project using Docker

To run a benchmark using a script, copy the script.json file:

```
cp script.json.template script.json
```

And execute the script:

```
benchmark.sh script <script_name>
```

To run all contracts available, run the following command passing the duration, type of fuzzing, and repetition times:

```
benchmark.sh <uri_or_folder> all 30m directed_greybox 1
```

## Running the project locally
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
