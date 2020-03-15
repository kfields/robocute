# RoboCute

## Installation

1. Navigate to a directory where you keep your software projects:

        cd projects

2. Clone the repository:

        git clone https://github.com/kfields/robocute.git
        
3. Navigate to the new directory which contains the repository.

        cd robocute

4. Create a Python 3 virtual environment called `env`:

        python3 -m venv env
        
5. Activate the environment:

        source env/bin/activate
        
6. Install required packages:

        pip install -r requirements.txt

## Extras
pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04  wxPython


## Development

1. Activate the virtual environment, if not already active:

        cd pugsley-lite
        source env/bin/activate
        
2. Launch the Flask application in debug mode:

        ./dev
