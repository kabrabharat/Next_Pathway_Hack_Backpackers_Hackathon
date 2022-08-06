'''
Pass sql query to find_columnName_and_tableAlias function for 
getting resultant column name and corresponding Table Alias

Under Process..

'''

# import libraries
import sqlparse
from sqlparse.tokens import DML


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