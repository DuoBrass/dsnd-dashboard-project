# Import the QueryBase class from query_base.py
from .query_base import QueryBase
# Import the execute_query function from sql_execution.py
from .sql_execution import execute_query, QueryMixin
# Define a subclass of QueryMixin and QueryBase
# called Employee
import pandas as pd  # To return SQL query results as a DataFrame
# Set the class attribute `name`
# to the string "employee"
class Employee(QueryMixin, QueryBase):
    name = "employee"  # Table name for the employee class

    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    def names(self):
        
        # Query 3
        # Write an SQL query
        # that selects two columns 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data
        # for all employees in the database
        query = f"""
            SELECT full_name, employee_id
            FROM {self.name}
        """
        return self.query(query)  # Executes the query via the mixin and returns a list of tuples

    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    def username(self, id):
        
        # Query 4
        # Write an SQL query
        # that selects an employees full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee
        # with an id equal to the id argument
        query = f"""
            SELECT full_name
            FROM {self.name}
            WHERE employee_id = {id}
        """
        return execute_query(query)  # Executes the query and returns a tuple

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    def model_data(self, id):
        query = f"""
            SELECT SUM(positive_events) AS positive_events
                 , SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING(employee_id)
            WHERE {self.name}.employee_id = {id}
        """
        result = execute_query(query)  # Execute the query
        return pd.DataFrame(result, columns=['positive_events', 'negative_events'])  # Convert to DataFrame
