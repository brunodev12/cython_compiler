# Cython Compiler
Script to compile Python in Cython files, making them faster.

# How it works
This script will compile all .py files in the run directory, including files in folders and subfolders.

Once compiled you can replace the original .py files of your program with the .so files that you will get here.

# Example

## Original program


        MyProgram/
        │   ├── utils/
        |   |   └── helpers.py
        │   └── src/
        │       ├── get_info.py
        │       └── connect.py
        |
        ├── main.py
        └── .env
      
## Compiled program


        MyProgram/
        │   ├── utils/
        |   |   └── helpers.so
        │   └── src/
        │       ├── get_info.so
        │       └── connect.so
        |
        ├── main.py
        └── .env

# Install and run the script

1. Install dependencies with pipenv: `pipenv install`

2. Compile files in place:

- Ubuntu: `python3 compile.py build_ext --inplace`
- Windows: `python compile.py build_ext --inplace`