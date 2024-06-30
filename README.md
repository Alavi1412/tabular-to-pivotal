# Tabular to Pivotal

This python package is designed to load forward quoted tabular data into pivotal data format. For now, this package only accept CSV files as input. But it is designed to be easily extended to load data from other sources.

## Installation

To install the package, run the following command in the root directory of the package:

```bash
pip install -e .
```

This will install the package in the current environment in editable mode. This means that any changes made to the source code will be reflected in the installed package without the need of reinstallation of the package during development.

This package requires Python 3.11 or later to run. It is recommended to use a virtual environment to install the package to avoid conflicts with other packages.

## Usage

There two ways to use the package:
- As a command line tool
- As a python package

### Command Line Tool

To use the package as a command line tool, put your input CSV file in the root directory of the package and run the following command:

```bash
tabular_to_pivotal input.csv output.csv
```

This command assumes that the input CSV file is named `input.csv` and then, it will create a new CSV file named `output.csv` in the root directory of the package.

### Python Package

To use the package as a python package, you can use the following code:

```python
from tabular_to_pivotal import load_and_transform

input_file = 'input.csv'
output_file = 'output.csv'

load_and_transform(input_file, output_file)
```

This code will load the data from the input CSV file, transform it into pivotal data format and save it in the output CSV file.

Attention: The library is not yet available on PyPi. To use it, you need to clone the repository and install it in editable mode as described in the installation section or you can add it in your project as a git submodule. Once it is available on PyPi, you will be able to install it using the normal pip install command.

## Development

To develop the package, you need to install the development dependencies. To do so, run the following command in the root directory of the package:

```bash
pip install -e .
```

The repository contains `launch.json` and `settings.json` files for Visual Studio Code. These files are used to configure the debugger for the package. To use the debugger, you need to install the Python extension in Visual Studio Code. Upon installation, you can run the debugger by putting your input CSV file with the name of `input.csv` in the root directory of the package and pressing `F5`. The debugger will run the code and stop at the breakpoints set in the code.
