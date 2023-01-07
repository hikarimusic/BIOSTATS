# Linux

## Virtual Environment
    python3 -m venv .biostats
    source .biostats/bin/activate

## Clone Repo
    git clone https://github.com/hikarimusic/BIOSTATS.git
    cd BIOSTATS
    pip install .
    biostats

## Build Package
    pip install --upgrade build
    python3 -m build

## Publish Package
    pip install --upgrade twine
    twine upload dist/*

## Build Executable
    pip install --upgrade pyinstaller
    python3 pyinstaller.py


# Windows

## Virtual Environment
    py -m venv .biostats
    .biostats\Scripts\activate.bat

## Clone Repo
    git clone https://github.com/hikarimusic/BIOSTATS.git
    cd BIOSTATS
    pip install .
    biostats

## Build Package
    pip install --upgrade build
    py -m build

## Build Executable
    pip install --upgrade pyinstaller
    py pyinstaller.py
