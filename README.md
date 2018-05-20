**Small python application for guest book.** 

This is a simple REST API application based on Flask framework.

_How to install_
```bash
git clone git@github.com:DmitryBurnaev/simple-guest-book.git guest_book
cd guest_book
python3 -m venv venv
source venv/bin/activate
pip install -r requiriments.txt

```
_How to test_
```bash
cd <path_to_projec>
source venv/bin/activate
(venv) $ python -m unittest

```
_How to run_

```bash
source venv/bin/activate
(venv) $ python src/app.py

```

_possible env variables_
```bash
FLASK_APP_HOST = 127.0.0.1
FLASK_APP_PORT = 5000
FLASK_DEBUG = False

```

