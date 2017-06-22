import pytest
import inspect

from API import Reference_section

class test_reference_section():

    def __int__(self):
        self.reference_section = Reference_section.Reference_section.initialize()

    def get_number_of_args(func):
        return len(func.func_code.co_varnames)

    def test_empty_reference_section(self):

        assert self.reference_section is not None

    def test_create_ref_with_less_arguments(self):

        ref_section = Reference_section.Reference_section.initialize('title', 'created')
    #    args = len(inspect.getargspec(create_reference_section('title', 'created')))
        assert ref_section is not None


    def test_create_ref_with_arguments(self):

#        Reference_section.Reference_section.initialize('Title', 'Creator', 'Created', 'Place')
        ref_section = Reference_section.Reference_section.initialize('Title', 'Creator', 'Created', 'Place', 'Contact')

        assert ref_section is not None


    def test_ref_object(self):
        assert isinstance(self.reference_section, Reference_section.Reference_section)


if __name__ == '__main__':
    pytest.main([__file__])


