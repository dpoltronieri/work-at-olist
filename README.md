# Welcome

This is the **[Work at Olist Challenge](Docs/Work_at_Olist.md)** wiki implemented by **Daniel Pereira Poltronieri**. It is the documentation and execution manual for the **Python Django** server and the database that accompanies it.

## About

This software uses the **Django** API and the **Django REST Framework** to implement the server.

## Development

The development ambient was an **Ubuntu Linux** installation with the **Atom** text editor.
All the tests are handled by the Django Unit Test Module, no test was done with selenium or other front end testing tool.

## Database

The database used was the default SQLite. Two models were implemented [here](Docs/Database.md)
A manager class was used to keep the database and views code DRY, [here](Docs/chargeManager.py.md).
The SQLite database prevents the app of being deployed to heroku, so pythonanywhere was used.

## Deployment

The server was deployed on pythonanywhere.com under the base url [http://dpoltronieri.pythonanywhere.com](http://dpoltronieri.pythonanywhere.com).
The *Debug = True* flag as a concious choice to facilitate the testing of this code in the evaluation round.

## Usage

The path urls are:

* calls/
  * **GET**: Get a complete list of completed calls on the database
  * **POST**: Send to the server data about a call
    * Type = Start: Obligatory to have the Call ID, source, destination and a timestamp or datetime string
    * Type = End: Obligatory to have the Call ID and a timestamp or datetime string. Will also calculate the charge and save to the database
* incomplete_calls/
  * **GET**: Get a complete list of incomplete calls
* bills/<string:source>/<int:year>/<int:month>/
  * **GET**: Gets a list of the destination, time of start and finish of the calls and price for each individual call on the period.
    * *Source*: The number of the bill
    * *Year*: The year in the form *YYYY*
    * *Month*: The month in the form *MM*
* bills/<string:source>/
  * **GET**: Gets a list of the destination, time of start and finish of the calls and price for each individual call on the last closed period.
    * *Source*: The number of the bill
