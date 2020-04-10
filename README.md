# songfinder

Type in a search term and find matching songs!

## Installation

To run this application locally, first make sure you have the following packages installed:
* gcc
* python3
* pip3

The application also requires the Musixmatch Dataset database, which can be downloaded [here](http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset.db). Place this file in the root folder of the application.

Then, in your local clone run:

```
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    flask run
```

Then visit http://127.0.0.1:5000 in your Web browser.

The first and second commands are necessary to create the virtual environment which contains the necessary python packages, which are listed in `requirements.txt`. On Windows machines, the second command is `venv\Scripts\activate` instead.
*THIS STEP IS IMPORTANT* because it prevents conflicts with other versions of the same packages required by different applications system-wide, and maintains application stability when these packages are upgraded system-wide.
To exit the virtual environment, use `deactivate`.

To run the application in development mode, allowing stack trace output inside your Web browser, add `FLASK_ENV=development` to `.flaskenv` or to your environment variables, whichever is more convenient.

### TODOS

* ~~Handle Musixmatch API response status 404~~
* Application crashes when searching for a word not in the top 5000 Musixmatch word list
* Handle response status codes that are not 200 or 404
* Allow a user-selected number of results per search
* Show the number of occurrences of the search term for each search result
