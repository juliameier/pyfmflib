import pytest
import inspect
import numpy

from API import Fmf



def test_empty_fmf():
        fmf_object = Fmf.FMF()
#        fmf_object.initialize()
        assert fmf_object is not None

 #       assert self.fmf_object is not None

def test_empty_fmf_instance():
        fmf_object = Fmf.FMF()
        assert isinstance(fmf_object, Fmf.FMF)

def test_create_fmf_with_reference():
        fmf_object = Fmf.FMF()
        fmf_object.set_reference('title', 'Creator', 'Created', 'Place', 'Contact')

        assert fmf_object is not None
#        assert isinstance(self.fmf_object, Fmf.FMF)


def test_create_fmf_with_table():
        fmf_object = Fmf.FMF()
        fmf_object.table_sections = [fmf_object.add_table('Table Name', 'Table Symbol')]

        assert fmf_object is not  None


def test_create_fmf_meta_section():
        fmf_object = Fmf.FMF()
        fmf_object.meta_sections = [fmf_object.add_meta_section('Name')]

        assert fmf_object is not None


if __name__ == '__main__':
    pytest.main([__file__])