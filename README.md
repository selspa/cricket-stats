
## To start the app run first `docker-compose build --no-cache` and then run `docker-compose up` 

### The app at the startup runs a migration to build the relational database and uses the 3 CSV files to fill the database. The functions in importCSVFunction.py use the data in the CSV files, select the relevant ones and insert them, normalised, into the db.
### Navigating into your browser to localhost:3000 you will be able to select a game and see the percentage of winning games and it will show an histogram with all the simulation runs
### It uses 3 containers: one for the database PostgreSQL, one with Python and one with React.js. The APIs are handled with FastAPI
