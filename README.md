# Retro snake server

Server for [Retro snake](https://github.com/Devoter/snake). Based on [bottle framework](https://github.com/bottlepy/bottle).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

* `git clone <repository-url>` this repository
* change into the new directory
* create virtualenv:
```bash
python3 -m venv env
source env/bin/activate
pip install wheel
pip install -r requirements.txt
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

## License

[MIT](LICENSE)
