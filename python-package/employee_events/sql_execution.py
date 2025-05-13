import sqlite3
from pathlib import Path
import pandas as pd
from functools import wraps

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path().resolve() / "employee_events.db"

# Define the function to execute SQL queries
def execute_query(query):
    with sqlite3.connect(db_path) as conn:
        result = pd.read_sql_query(query, conn)  # Execute the query and return as pandas DataFrame
    return result

# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query):
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query(sql_query, conn)

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            result = cursor.execute(sql_query).fetchall()
        return result


# Define a new class called `QueryBase` with the methods you need
class QueryBase:
    # Class attribute
    name = ""  # Set the class attribute to an empty string

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        return []

    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):
        query = f"""
            SELECT event_date, 
                   SUM(CASE WHEN event_type = 'positive' THEN 1 ELSE 0 END) AS positive_events,
                   SUM(CASE WHEN event_type = 'negative' THEN 1 ELSE 0 END) AS negative_events
            FROM {self.name}
            WHERE employee_id = ?
            GROUP BY event_date
            ORDER BY event_date;
        """
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()
        return df

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):
        query = f"""
            SELECT note_date, note
            FROM notes
            WHERE employee_id = ?
            ORDER BY note_date;
        """
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()
        return df


# Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query