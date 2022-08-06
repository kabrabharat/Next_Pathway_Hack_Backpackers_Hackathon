'''
Pass sql query to find_columnName_and_tableAlias function for 
getting resultant column name and corresponding Table Alias

Under Process..

'''

# import libraries
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML


def find_columnName_and_tableAlias(sql : str) -> dict:
    '''
        Description:
        -----------
        Function intake sql query and return the resultant columns and it's table name

        Parameters:
        ---------
        sql (str) : Input Sql Query in string format

        Returns:
        columns_alias (dict) : Dictionary Containing Column name and respective Table name
        -------

    '''

    # parsing sql query to sqlparse to get tokens
    sql_parsed = sqlparse.parse(sql)[0]
    
    # for checking SELECT DML Keyword
    found_select = False

    # to store resultant dictionary
    columns_alias = {}
    flag_select = 1

    # iterating on sql tokens
    for token in sql_parsed.tokens:
        if found_select:
            # checking if tokens are IdentifierList or Identifier, and flag_select is to get just the first SELECT statement in query
            if (isinstance(token, sqlparse.sql.IdentifierList) or isinstance(token, sqlparse.sql.Identifier)) and flag_select ==1 :
                
                # handling in case of multiple columns
                if len(token.value.split(','))>1:
                    
                    for col in token.tokens:
                        # checking if the token type is Identifier
                        if isinstance(col, sqlparse.sql.Identifier):
                            # storing columns and tablename alias in key value format
                            columns_alias[col.value.split(" ")[-1].strip("`").rpartition('.')[-1]] = col.value.split(" ")[-1].strip("`").rpartition('.')[0]
                else:
                    columns_alias[token.value.split(" ")[-1].strip("`").split('.')[-1]] = [token.value.split(" ")[-1].strip("`").split('.')[0]]
                flag_select = 0
        # if found select statement then after that token only above if condition will work
        elif token.ttype is DML and token.value.upper() == 'SELECT':
            found_select = True

    return columns_alias

def is_subselect(parsed: sqlparse.sql.Statement) -> bool:
    '''
        Description:
        -----------
        Function to iterate and check for first SELECT statement 

        Parameters:
        ---------
        parsed (sqlparse.sql.Statement) : parsed sql statement object

        Returns:
        True/False (bool) : Boolean value
        -------

    '''
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_from_part(parsed: sqlparse.sql.Statement) -> object:
    '''
        Description:
        -----------
        Recursive function to check statements after FROM keyword 

        Parameters:
        ---------
        parsed (sqlparse.sql.Statement) : parsed sql statement object

    '''
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                yield from extract_from_part(item)
            elif item.ttype is Keyword:
                return
            else:
#                 print(type(item))
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers(token_stream : list) -> dict:
    '''
        Description:
        -----------
        extract tablenames and it's alias 

        Parameters:
        ---------
        token_stream (list) : list of sql parsed objects

        Returns:
        -------

        tables (dict): dictionary containing tablenames and it's alias as key, value pair

    '''
    tables = {}
    for item in token_stream:

        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                tables[identifier.get_name()] = identifier.value.split(" ")[:-1][identifier.value.split(" ")[:-1].index('FROM')+1].strip('(').strip(')')
                
                yield tables                  


def get_originating_tables(sql_script: str) -> str:
    """
    Description :
    ----------- 
    Function to extract the resultant table names and column names

    Parameters:
    ----------
    sql_script (str): string containing sql statement

    Returns:
    -------
    final_sql (str): desired output of table names and column names
    

    """
    columns = find_columnName_and_tableAlias(sql_script)
    stream = extract_from_part(sqlparse.parse(sql_script)[0])
    tables = dict(list(extract_table_identifiers(stream))[0])
    final_sql = "column => table\n"
    
    for key, value in columns.items():
        final_sql += str(columns[key]) + " => " + str(tables[value]) + "\n"

    return final_sql