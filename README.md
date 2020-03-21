# RoboCute

## Installation

Navigate to a directory where you keep your software projects

        cd projects

Clone the repository

        git clone https://github.com/kfields/robocute.git
        
Navigate to the new directory which contains the repository

        cd robocute

Create a Python 3 virtual environment called `env`

        python3 -m venv env
        
Activate the environment

        source env/bin/activate
        
Install required packages

        pip install -r requirements.txt

## Extras
pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04  wxPython


## Run

Activate the virtual environment, if not already active

        cd robocute
        source env/bin/activate
        
Run the game

        python main.py
