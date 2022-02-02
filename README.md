1) Create virtual environment, all library in the file 'requirements.txt'
2) Run the file 'report.py' to get report

# Parser base on scrapy

Scrapy is a Python framework for parsing site.\
This parser parse site: https://blog.griddynamics.com/ and get the report

## Installation

Create virtual environment, all library in the file 'requirements.txt'

1) If you don`t have library 'virtualenv', use the package manager [pip](https://pip.pypa.io/en/stable/) to install
   'virtualenv'.
```bash
python3 -m pip install virtualenv
```
2) Create and activate your virtual environment
```bash
virtualenv [name of your new virtual environment]
source [name of your new virtual environment]/bin/activate
```
3) Install all library from the file 'requirements.txt'
```bash
python3 -m pip install -r GridBlog/requirements.txt
```
## Usage
To start project run command
```bash
cd GridBlog/
python3 report.py
```
