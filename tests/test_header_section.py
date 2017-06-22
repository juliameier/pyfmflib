import encodings

import pytest
from API import Header_section

class test_header_section():

    def __int__(self):
        self.header_section = Header_section.Header.initialize()

    def test_create_header(self):
#       create_header_section()
        header_section = Header_section.Header.initialize('fmf-version:1.0', 'utf-8', '\t', ';')

        assert header_section is not None

if __name__ == '__main__':
    pytest.main([__file__])
