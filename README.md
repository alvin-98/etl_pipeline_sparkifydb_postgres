
# ETL Pipeline for a Music App Startup
The project uses python and sql to create an ETL pipeline for a music app startup. Sparkify collects data on their songs and user activity in their app into two local databases. Data on the song tracks and their artists are stored in song dataset and user logs are stored in log dataset. We create a postgres database with fact and dimension tables in a star schema. This is because we want a database that is optimized particularly for song play analytics. As a result, we can do fast aggregations and write simple queries to get insights on song plays.


## How to Use?

1. Download the repository to your local system.
2. Install libraries mentioned in the requirements.txt file using command prompt.
        >pip install library_name
3. Run the 'create_tables.py' file on command prompt using the below command to create the sparkify database and relevant tables.
        >python create_tables.py
4. Run the 'etl.py' file on command prompt using the below command to run the ETL pipeline and load the data into respective tables in the database.
        >python etl.py


## Files in Repository

1. create_tables.py
Creates the Sparkify database, drops any existing tables with the same names and then creates all relevant tables, according to defined schema, afresh.
2. sql_queries.py
Contains SQL queries for CREATE TABLE, INSERT, SELECT, and DROP as strings to be used by the create_tables.py file.
3. etl.py
Implements the ETL pipeline
4. test.ipynb
An interactive python notebook which can be used to test the functioning of the ETL pipeline.
5. etl.ipynb
An interactive python notebook which can be used to experiment with the ETL pipeline code before finalizing code for production.
