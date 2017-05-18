import pytest
import inspect

class FMF():

    def __init__(self, header, meta_sections, tables, global_comments, compliance_level):

        self.header = header
        self.meta_sections = meta_sections
        self.table_sections = tables
        self.global_comments = global_comments
        self.compliance_level = compliance_level

class FMF2():

    def __init__(self, name):

        self.name = name

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


class Meta_section():

    def __int__(self, name, entries, comments):

        self.name = name
        self.entries = entries
        self.comments = comments

class Meta_section_entry():

    def __int__(self, key, value):

        self.key = key
        self.value = value

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

class Header():

    def __init__(
            self,
            fmf_version,
            encoding,
            field_separator,
            comment_character
    ):

        self.fmf_version = fmf_version
        self.encoding = encoding
        self.field_separator = field_separator
        self.comment_charater = field_separator


def create_fmf(*args, **kwargs):

    # args represents the regular arguments
    # kwargs represents the keyword arguments
    print args, kwargs
    print (len(args))
    print (len(kwargs))

    return FMF(header=None, meta_sections=[], tables=[], global_comments=[], compliance_level=None)

def create_meta_section(*args):

    print args

    return Meta_section(name=None, entries=[], comments=[])


class MissingSubmissionException(Exception):
    pass

def create_reference_section(*args):

    # args represents the regular arguments
    # kwargs represents the keyword arguments
    print args

    print len(args)

    if len(args) > 0 and len(args) < 4:
        raise MissingSubmissionException('Mandatory keyword or parameter is missing')

    return Reference_section(title=None, creator=None, created=None, place=None, contact=None)


def create_table_object(*args):

    print (args)
    print (len(args))

    if len(args) < 2:
        raise Exception('Number of arguments specified is invalid')

    return Table(name=None, symbol=None, data_definitions=[], no_columns=None, no_rows=None, data=[], comments=None)


#create_fmf('fmf-version: 1.0', compliance_level=1)

create_fmf(title='title', creator='Creator', created='Created', place='Place')

def test_create_fmf():
    #Create an empty FMF object
    create_fmf()

def test_create_fmf_with_arguments():
    create_fmf(title='title', creator='Creator', created='Created', place='Place')
#    inspect.getargspec(create_fmf('fmf-version: 1.0', compliance_level=1))


def test_fmf_object():
    assert isinstance(create_fmf(), FMF)


def test_fmf_object2():
    assert isinstance(create_fmf('fmf-version: 1.0', compliance_level=1), FMF)



def test_set_reference():
    fmf_object = create_fmf()

    fmf_object.meta_sections = [create_reference_section(
       'Title', 'Creator','Created','Place' )]

def test_add_table():
    fmf_object = create_fmf()

    fmf_object.table_sections = [create_table_object('Table Name', 'Table Symbol')]


def test_create_meta_section():
    create_meta_section()


if __name__ == '__main__':
    pytest.main([__file__])
