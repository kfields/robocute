# RoboCute :robot:

This is a game I wrote for [PyWeek #6](https://pyweek.org/)

## Quick Start

```bash
git clone https://github.com/kfields/robocute.git

cd robocute

poetry shell

poetry install

python main.py
```

## wxPython Integration

Since there aren't any binary wheels for wxPython,  I leave this to you, the reader.
In short, it takes a long time to build. :(

### Ubuntu

```bash
sudo apt install libgtk-3-dev
pip install wxPython

python mainwx.py
```