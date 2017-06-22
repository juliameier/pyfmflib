import pytest
import inspect
import numpy

from API import Fmf

class test_fmf():

    def __int__(self):
        self.fmf_object = Fmf.FMF.initialize()


    def test_empty_fmf(self):

        assert self.fmf_object is not None

    def test_empty_fmf_instance(self):

        assert isinstance(self.fmf_object, Fmf.FMF)

    def test_create_fmf_with_reference(self):

        self.fmf_object = Fmf.set_reference(title='title', creator='Creator', created='Created', place='Place')

        assert self.fmf_object is not None
#        assert isinstance(self.fmf_object, Fmf.FMF)


    def test_create_fmf_with_table(self):

        self.fmf_object.table_sections = [Fmf.add_table('Table Name', 'Table Symbol')]


    def test_create_fmf_meta_section(self):

        self.fmf_object.meta_sections = [Fmf.add_meta_section('Name')]
        

if __name__ == '__main__':
    pytest.main([__file__])
