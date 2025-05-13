import sqlite3
import pandas as pd

# Define the QueryBase class
class QueryBase:
    # Class attribute
    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""  # Set the class attribute to an empty string

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        # Return an empty list by default
        return []

    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):
        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        conn = sqlite3.connect('employee_events.db')  # Update with the actual database path
        query = f"""
            SELECT event_date,
                   SUM(CASE WHEN event_type = 'positive' THEN 1 ELSE 0 END) AS positive_events,
                   SUM(CASE WHEN event_type = 'negative' THEN 1 ELSE 0 END) AS negative_events
            FROM {self.name}
            WHERE employee_id = ?
            GROUP BY event_date
            ORDER BY event_date;
        """
        # Execute the query with the id argument
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()
        return df

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):
        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        conn = sqlite3.connect('employee_events.db')  # Update with the actual database path
        query = f"""
            SELECT note_date, note
            FROM {self.name}_notes
            WHERE employee_id = ?
        """
        # Execute the query with the id argument
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()
        return df
            
    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):
        

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        conn = sqlite3.connect('employee_events.db')  # Update with the actual database path
        query = f"""
            SELECT note_date, note
            FROM {self.name}_notes  # Assumes the notes table follows this naming convention
            WHERE employee_id = ?
        """
    # Execute the query with the id argument
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()
        return df

