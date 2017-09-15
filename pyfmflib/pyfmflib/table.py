class Table(object):

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

    def initialize(*args):

        print (args)
        print (len(args))

        if len(args) < 2:
            raise Exception('Number of arguments specified is invalid')

        return Table(name=None, symbol=None, data_definitions=[], no_columns=None, no_rows=None, data=[], comments=None)

