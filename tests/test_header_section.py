import encodings

import pytest

class Header():

    def __init__(
            self,
            fmf_version,
            encoding,
            separator,
            comment_char,
            misc_params
    ):

        self.fmf_version = fmf_version
        self.encoding = encoding
        self.field_separator = separator
        self.comment_char = comment_char
        self.misc_params = misc_params



def create_header_section(*args):

    print args

    print len(args)

    if len(args) < 4:
        raise Exception('Mandatory keyword or parameter is missing')

    return Header(fmf_version=None, encoding=None, separator=None, comment_char=None, misc_params=None)

def test_create_header():
#    create_header_section()
    create_header_section('fmf-version:1.0', 'utf-8', '\t', ';')

if __name__ == '__main__':
    pytest.main([__file__])
