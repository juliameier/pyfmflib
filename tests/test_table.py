import pytest

class Table():

    def  __init__(
            self,
            name,
            symbol,
            data_definitions,
            no_columns,
            no_rows,
            data,
            comments
    ):

        self.name = name
        self.symbol = symbol
        self.data_definitions = data_definitions
        self.no_columns = no_columns
        self.no_rows = no_rows
        self.data = data
        self.comments = comments

def create_table_object(*args):

    print (args)
    print (len(args))

    if len(args) < 2:
        raise Exception('Number of arguments specified is invalid')

    return Table(name=None, symbol=None, data_definitions=[], no_columns=None, no_rows=None, data=[], comments=None)

def test_create_table():
    create_table_object()

def test_table_object():
    assert isinstance(create_table_object(), Table)

def test_table_with_arguments():

    # Specifying less arguments
#    create_table_object('Name')

    # Specifying the minimum 2 arguments
    create_table_object('Name', 'Symbol')


if __name__ == '__main__':
    pytest.main([__file__])
