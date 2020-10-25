# CS235Flix

## Description

A Netflix clone developed to browse movies.

## Installation

**Installation via requirements.txt**

```shell
$ cd CS235Flix
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:CS235Flix' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment.
## Execution

**Running the application**

From the CS235Flix directory, and within the activated virtual environment (see venv\Scripts\activate above):

````shell
$ flask run
```` 


## Configuration

The *CS235Flix/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

**Testing the application**

From the CS235Flix directory, and within the activated virtual environment (see venv\Scripts\activate above):

````shell
$ python -m pytest
```` 

I've also included a nifty .bat file for starting the virtual environment, running the test program, and closing the virtual environment.
Simply double click the .bat file to run the command (in Windows) and it'll execute the commands automatically.
 