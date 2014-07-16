# -*- coding: utf-8 -*-

# Copyright (c) 2014, Rectorate of the University of Freiburg
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
from pyfmflib import cl1
from fixtures import (
    empty_fmf, fmf_template, meta_section, fmf_template_with_tables
    )


def test_create_empty_fmf():
    # create a completely empty fmf instance, e.g. as a stream destination
    cl1.new_empty_fmf()


def test_create_fmf_template():
    # create a minimal (formally) valid fmf
    cl1.new_fmf_template()


def test_create_minimal_fmf():
    # create an fmf with minimal meta data
    cl1.new_minimal_fmf(
        title='Title',
        creator='Creator',
        created='Timestamp',
        place='Location'
        )


def test_create_fmf_with_default_header():
    # create an empty fmf with only the default header
    fmf = cl1.new_fmf_with_default_header()
    assert fmf.header == cl1.Header()


def test_set_header(empty_fmf):
    empty_fmf.header = cl1.Header()


def test_set_reference_section(empty_fmf):
    empty_fmf.meta_sections = [
        cl1.new_minimal_reference_section(
            creator='Creator',
            created='Timestamp',
            title='Title',
            place='Place'
            )
        ]


def test_add_comments_before_first_section(fmf_template):
    from pyfmflib.cl1 import Comment
    fmf_template.global_comments = [Comment('Comment 1'), Comment('Comment 2')]


def test_add_meta_section(fmf_template, meta_section):
    fmf_template.meta_sections.append(meta_section)


def test_get_meta_section_by_identifier(fmf_template, meta_section):
    fmf_template.meta_sections.append(meta_section)
    assert fmf_template[meta_section.identifier] == meta_section


def test_equality():
    assert cl1.new_fmf_template() == cl1.new_fmf_template()


def test_add_single_anonymous_table(empty_fmf):
    from pyfmflib.cl1 import DataDefinitions, Data, KeyValue, Comment, DataRow
    empty_fmf.table_sections = [
        DataDefinitions(
            symbol=None,  # default value, just to illustrate
            entries=[
                KeyValue('time', 't [s]'),
                KeyValue('distance', 's(t) [m]'),
                Comment('useless comment')
                ]
        ),
        Data(
            symbol=None,
            entries=[
                Comment('t / s    s(t) / m'),
                DataRow(('0', '-2')),
                DataRow(('1.1', '0.1')),
                DataRow(('2.0', '3.1')),
                DataRow(('2.9', '4.5')),
                ]
            )
        ]


def test_add_multiple_tables(empty_fmf):
    from pyfmflib.cl1 import (
        TableDefinitions, DataDefinitions, Data, KeyValue, DataRow
        )
    empty_fmf.table_sections = [
        TableDefinitions(
            [
                KeyValue('Table 1', 't_1'),
                KeyValue('Table 2', 't_2'),
                ]
            ),
        DataDefinitions(
            symbol='t_1',
            entries=[
                KeyValue('time', 't [s]'),
                KeyValue('distance', 's(t) [m]'),
                ]
        ),
        Data(
            symbol='t_1',
            entries=[
                DataRow(('0', '-2')),
                DataRow(('1.1', '0.1')),
                DataRow(('2.0', '3.1')),
                DataRow(('2.9', '4.5'))
                ]
            ),
        DataDefinitions(
            symbol='t_2',
            entries=[
                KeyValue('another time', 't [ms]'),
                KeyValue('another distance', 's(t) [mum]'),
                ]
        ),
        Data(
            symbol='t_2',
            entries=[
                DataRow(('1', '2')),
                DataRow(('2.1', '3.4'))
                ]
            )
        ]


def test_get_table_sections(fmf_template_with_tables):
    # do we need more functionality on CL1 than just
    # dealing with the list of sections?
    # should we be able to assemble table objects from
    # the sections and vice versa on CL1?
    table_sections = fmf_template_with_tables.table_sections
    assert len(table_sections) > 0
    if isinstance(table_sections[0], cl1.TableDefinitions):
        # we have named tables
        pass
    else:
        # a single anonymous table
        pass


def test_create_whole_fmf():
    from pyfmflib.cl1 import (
        FMF, Header, Comment, MetaSection, KeyValue,
        DataDefinitions, Data, DataRow, ReferenceSection,
        Creator, Created, Title, Place
        )
    FMF(
        header=Header(),
        global_comments=[
            Comment('A comment'),
            Comment('Another Comment')
            ],
        meta_sections=[
            ReferenceSection(
                [
                    Creator('Creator'),
                    Comment('A Comment'),
                    Created('Timestamp'),
                    Title('Title'),
                    Place('Place')
                    ]
                ),
            MetaSection(
                identifier='A Section',
                entries=[
                    Comment('A comment'),
                    KeyValue('a', 'b')
                    ]
                ),
            MetaSection(
                identifier='Another Section',
                entries=[KeyValue('c', 'd')]
                ),
            ],
        table_sections=[
            DataDefinitions(
                entries=[
                    KeyValue('time', 't [s]'),
                    KeyValue('distance', 's(t) [m]'),
                    Comment('useless comment')
                    ]
                ),
            Data(
                symbol=None,
                entries=[
                    Comment('t / s    s(t) / m'),
                    DataRow(('0', '-2')),
                    DataRow(('1.1', '0.1')),
                    DataRow(('2.0', '3.1')),
                    DataRow(('2.9', '4.5')),
                    ]
                )
            ]
        )


if __name__ == '__main__':
    pytest.main([__file__])
