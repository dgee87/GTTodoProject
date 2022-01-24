# Searching for TODOs

The following `python` program searches for list of files in directories and sub-directories that contains `"TODO"`.

The application uses the design pattern [Strategy](https://refactoring.guru/design-patterns/strategy) to highlight 
that there could be multiple ways to search for a certain text in a text file of arbitary size.

## Pre-requisites

* Docker
* Python >= 3.7

## How to Run

There are 2 main ways you can run the project, via python setup or docker script as described in below sections.
This project does not require any pip installation, except when running tests.

### How to Run - Using Python

Once you have a python environment setup, you can navigate to the project directory and execute this command:

```commandline
$ python main.py
```

You can set [configurations](#configurations) using the `export` command, example:

```commandline
$ export ENCODING=utf-8
$ export WHITE_LIST_DIR=.git,.idea
$ python main.py
```

### How to Run - Using Docker Script

If you have docker installed, just run this from the main project directory:

```commandline
$ sh scripts/run_main.sh
```

## Output results example

Successful run with python `main.py` will output list of files as below:

```text
****************************************
List of TODO files: 6
<path_to_your_dir>/GTTodoProject/main.py
<path_to_your_dir>/GTTodoProject/README.md
<path_to_your_dir>/GTTodoProject/somedir3/another_file.js
<path_to_your_dir>/GTTodoProject/somedir2/anotherdir/index.js
<path_to_your_dir>/GTTodoProject/somedir2/anotherdir/yetanotherdir/index.js
<path_to_your_dir>/GTTodoProject/somedir/somemodule/someotherfile.js
****************************************
```

Take note, your output might differ from the above if you have provided your own configurations.

## Output results example with Dockerfile

If running with docker script, take note that the path directory prefix starts from `/home/project`.
This is because we set the working directory as it is, all underlying directories and sub-directories remain unchanged.

Example output:  

```text
****************************************
List of TODO files: 6
/home/project/README.md
/home/project/main.py
/home/project/somedir3/another_file.js
/home/project/somedir2/anotherdir/index.js
/home/project/somedir2/anotherdir/yetanotherdir/index.js
/home/project/somedir/somemodule/someotherfile.js
****************************************
```

## Test Coverage

To run the python tests with coverage, make sure you have `nose` and `coverage` installed:

```commandline
$ pip install nose && pip install coverage
```

Then execute this command from the project directory:

```commandline
$ nosetests --tests=tests -v --nologcapture --exe --with-xunit --with-coverage
```

Alternatively, if you have docker installed, simply run the test shell script here:

```commandline
$ sh scripts/run_unittest.sh
```

You should see an output similar to the below:

```text
test_1_simple_find_strategy_found (tests.test_search.TestSearch) ... ok
test_2_buffer_find_strategy_found (tests.test_search.TestSearch) ... ok
test_3_buffer_find_strategy_not_found (tests.test_search.TestSearch) ... ok
test_4_search_context (tests.test_search.TestSearch) ... ok
test_5_search_client (tests.test_search.TestSearch) ... ok
test_err_1_unavailable_strategy (tests.test_search.TestSearch) ... ok


Name                   Stmts   Miss  Cover
------------------------------------------
main.py                  100      0   100%
tests/__init__.py          0      0   100%
tests/test_search.py      45      0   100%
------------------------------------------
TOTAL                    145      0   100%
----------------------------------------------------------------------
Ran 6 tests in 0.093s

OK

```

## Configurations

The following configurations can be set in the file `docker_env`:

| Name | Default Value | Description |
|---------------|---------------|---------------|
| ENCODING | 'utf-8'  | Unicode value to use for reading the files  |
| SEARCH_STRATEGY | 'simple'  | Possible values: `simple`, `buffer`  |
| CHUNK_SIZE | 4096  | Used to read large files in chunks, only if `SEARCH_STRATEGY` is `buffer`  |
| WHITE_LIST_DIRS | ".git,.idea"  | List of directories to ignore for the search context  |
| CONCURRENCY | 1  | Concurrency threads of workers to read the files  |