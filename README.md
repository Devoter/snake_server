# Retro snake server

Server for [Retro snake](https://github.com/Devoter/snake). Based on [bottle framework](https://github.com/bottlepy/bottle).

## Installation

* `git clone <repository-url>` this repository
* change into the new directory
* create virtualenv:
```bash
python3 -m venv env
source env/bin/activate
pip install wheel
pip install -r requirements
```

## Hash

Hash function is required to communicate with the client. You can use default encrypt function:
```bash
cp encrypt.example.py encrypt.py
```

## Start

```bash
python server.py
```
