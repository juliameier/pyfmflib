# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2017, Rectorate of the University of Freiburg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the Freiburg Materials Research Center,
#   University of Freiburg nor the names of its contributors may be used to
#   endorse or promote products derived from this software without specific
#   prior written permission.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import pytest
import numpy

from pyfmflib import table, fmf, meta_section

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
