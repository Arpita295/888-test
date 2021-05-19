# 888-test

## Setting up

```
1.Install MySQL server
2.pip install mysql-connector-python
```

## Running crud app code from command-line/terminal

```
$ python crud.py create/read/update <table_name> (provide username,password and hostname for SQL when prompted)
$ python crud.py --help (For help)
$ python -m unittest test_crud_app.TestCrudApp
```

## Alternatively test from pycharm
```
1.Open Project
2.Open Terminal
3.python crud.py create/read/update <table_name>
4.test_crud_app.py -> Run 'Unittests in test_crud...'

```

## Log file

```
Log file created as crup_app.log in the same folder

```