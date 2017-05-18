import pytest
import inspect

class Reference_section():

    def  __init__(
            self,
            title,
            creator,
            created,
            place,
            contact
    ):

        self.title = title
        self.creator = creator
        self.created = created
        self.place = place
        self.contact = contact


def create_reference_section(*args):

    # args represents the regular arguments
    # kwargs represents the keyword arguments
    print args

    print len(args)

    if len(args) > 0 and len(args) < 4:
        raise Exception('Number of arguments specified is invalid')

    return Reference_section(title=None, creator=None, created=None, place=None, contact=None)


def get_number_of_args(func):
    return len(func.func_code.co_varnames)

def test_create_reference_section():
    create_reference_section()

def test_create_ref_with_less_arguments():
    create_reference_section('title', 'created')
#    args = len(inspect.getargspec(create_reference_section('title', 'created')))

def test_create_ref_with_arguments():
    create_reference_section('Title', 'Creator', 'Created', 'Place')
    create_reference_section('Title', 'Creator', 'Created', 'Place', 'Contact')


def test_ref_object():
    assert isinstance(create_reference_section(), Reference_section)


if __name__ == '__main__':
    pytest.main([__file__])


