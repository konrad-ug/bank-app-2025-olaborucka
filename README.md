[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name: Aleksandra

surname: Borucka

group: 1

## How to start the app
python -m venv venv
source venv/bin/activate

export PYTHONPATH=.:$PYTHONPATH && flask --app app/api.py run


## How to execute tests
python3 -m coverage run --source=src -m pytest tests/unit && python3 -m coverage report -m
behave
python3 -m pytest tests/api
