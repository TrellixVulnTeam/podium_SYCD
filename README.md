Home of the **TakeLab Podium** project. 

## System prerequisites

- ```virtualenv```
- ```python3.6```
- ```pip```

## Building and running unit tests

You will work in a virtual environment and keep a list of required
dependencies in a ```requirements.txt``` file. The master branch of the 
project **must** be buildable with passing tests **all the time**. 

```

virtualenv -p python3.6 env
source env/bin/activate
pip install -r requirements.txt
python -m pytest

```

## Adding new dependencies

Adding a new framework to a project should be done via ```pip install
<new_framework>```. **Don't forget to add it to requirements.txt** 

## Details

The project is packaged according to official Python packaging
[guidelines](https://packaging.python.org/tutorials/packaging-projects/).

## Project package TODOs

- The project still needs a to have a license picked. 
- Windows and OSX instructions on installation and building
