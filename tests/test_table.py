import pytest
import numpy

from API import Table, Fmf,Meta_section

class test_table():

    def __int__(self):
        self.table = Table.Table.initialize()

    def test_create_table(self):
        assert self.table is not None

    def test_table_object(self):
        assert isinstance(self.table, Table.Table)

    def test_table_with_arguments(self):

        # Specifying less arguments
    #    create_table_object('Name')

        # Specifying the minimum 2 arguments
        Table.initialize('Name', 'Symbol')

        assert Table is not None

    def test_add_table_with_data(self):
        fmf_object = Fmf.initialize()

        fmf_object.table_sections = [
            Table.initialize('Table Name', 'Table Symbol',
                            data_definitions=[
                                Meta_section.Meta_section_entry.initialize('voltage', 'V [V]'),
                                Meta_section.Meta_section_entry.initialize('current', 'I(V) [A]')],

                            no_columns = 2,
                            no_rows = 3,

                            data = numpy.array([[1, 2], [3, 4], [5,6]], numpy.int32)
                            )
    ]




if __name__ == '__main__':
    pytest.main([__file__])
