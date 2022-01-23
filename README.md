# Searching for TODOs

The following `python` program searches for list of files in directories and sub-directories that contains `"TODO"`.

## How to Run

## Configurations

The following configurations can be set in the file `docker_env`:

| Name | Default Value | Description |
|---------------|---------------|---------------|
| ENCODING | 'utf-8'  | Unicode value to use for reading the files  |
| SEARCH_STRATEGY | 'simple'  | Possible values: `simple`, `buffer`  |
| CHUNK_SIZE | 4096  | Used to read large files in chunks, only if `SEARCH_STRATEGY` is `buffer`  |
| WHITE_LIST_DIRS | ".git,.idea"  | List of directories to ignore for the search context  |
| CONCURRENCY | 1  | Concurrency threads of workers to read the files  |