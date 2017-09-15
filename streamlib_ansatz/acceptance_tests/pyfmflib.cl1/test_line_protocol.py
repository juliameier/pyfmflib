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
from fixtures import lstream, lhstream, lhrstream
from pyfmflib.cl1 import (
    Header, Comment, SectionHeader, KeyValue, DataRow, END_FMF,
    ReferenceSectionHeader, Title, Creator, Created, Place,
    MetaSectionHeader, DataDefinitionsHeader, DataHeader,
    format_data_row, TableDefinitionsHeader, columns2rows, DataColumn
    )


def test_whole_fmf_raw_protocol(lstream):

    lstream.inject_packets(
        [
            Header(),

            Comment('A comment'),

            SectionHeader('*reference'),
            KeyValue('title', 'Title'),
            KeyValue('creator', 'Creator'),
            KeyValue('created', 'Timestamp'),
            KeyValue('place', 'Place'),

            SectionHeader('My Section'),
            KeyValue('x', '1.3'),
            KeyValue('important parameter', r'\eta = 1.24e-9 mW'),

            SectionHeader('*table definitions'),

            KeyValue('table1', 't_1'),
            KeyValue('table2', 't_2'),

            SectionHeader('*data definitions: t_1'),
            KeyValue('distance', 'd [m]'),
            KeyValue('time', 't [s]'),

            SectionHeader('*data: t_1'),
            Comment('d    t'),
            DataRow(("2.3", "4.555")),
            DataRow(("1.2", "4.15")),

            SectionHeader('*data definitions: t_2'),
            KeyValue('Energy', 'E [J]'),
            KeyValue('distance', 'd [m]'),

            SectionHeader('*data: t_2')
            ]
        )

    lstream.inject_packets(
        cl1.columns2rows(
            (
                cl1.DataColumn(("1.2", "1.3", "1.5", "1.6")),
                cl1.DataColumn(("2.2", "2.3", "2.5", "2.6"))
                )
            )
        )

    lstream.inject_packet(END_FMF)


# -- tests for convenience methods below --


def test_inject_default_header(lstream):
    lstream.inject_packet(Header())


def test_inject_custom_header(lstream):
    lstream.inject_packet(
        Header(
            coding='latin-1',
            fmfversion='1.0',
            comment_char='#',
            delimiter='whitespace',
            extra_parameters={'foo': 'bar', 'baz': 'kaz'}
            )
        )


def test_inject_comments(lhstream):
    lhstream.inject_packets(
        [
            Comment('a comment'),
            Comment('another comment')
            ]
        )


def test_inject_reference_section(lhstream):
    lhstream.inject_packets(
        [
            ReferenceSectionHeader(),
            Title('Title'),
            Creator('Creator'),
            Comment('Invalid time stamp:'),
            Created('just now'),
            Place('Place'),
            ]
        )


def test_inject_meta_section(lhrstream):
    lhrstream.inject_packets(
        [
            MetaSectionHeader('My Section'),
            KeyValue('x', '1.3'),
            KeyValue('important parameter', r'\eta = 1.24e-9 mW'),
            KeyValue('s', '"string value"')
            ]
        )


def test_inject_anonymous_table(lhrstream):
    lhrstream.inject_packets(
        [
            DataDefinitionsHeader(),
            KeyValue('distance', 'd [m]'),
            KeyValue('time', 't [s]'),

            DataHeader(),
            Comment('d    t'),
            DataRow(("2.3", "4.555")),
            DataRow(("1.2", "4.15"))
            ]
        )


def test_inject_tables(lhrstream):
    lhrstream.inject_packets(
        [
            TableDefinitionsHeader(),
            KeyValue('table1', 't_1'),
            KeyValue('table2', 't_2'),

            DataDefinitionsHeader('t_1'),
            KeyValue('distance', 'd [m]'),
            KeyValue('time', 't [s]'),

            DataHeader('t_1'),
            Comment('d    t'),
            DataRow(("2.3", "4.555")),
            DataRow(("1.2", "4.15")),

            DataDefinitionsHeader('t_2'),
            KeyValue('Energy', 'E [J]'),
            KeyValue('distance', 'd [m]'),

    # data streaming examples:
    # ------------------------

            DataHeader('t_2'),
            DataRow(("2.3", "1.33")),
            DataRow(["100.2", "44.2"]),

            format_data_row((2.3, 4.555), lambda x: '%.2f' % (x, ))
            ]
        )
    # Stream columns that are all known at a time.
    # For sequential streaming see test_column_data_protocol.py
    lhrstream.inject_packets(
        cl1.columns2rows(
            (
                cl1.DataColumn(("1.0", "3.4", "5.2")),
                cl1.DataColumn(("2.0", "2.4", "2.2")),
                )
            )
        )

    # stream nested iterable
    lhrstream.inject_packets(
        cl1.rowmajor2rows(
            (
                ('0', '-2'),
                ('1.1', '0.1'),
                ('2.0', '3.1'),
                ('2.9', '4.5')
                )
            )
        )

    # use a formatter:
    lhrstream.inject_packets(
        cl1.columnmajor2rows(
            (
                (0, 1.1, 2.0, 2.9),
                (-2, 0.1, 3.1, 4.5)
                ),
            formatter=lambda x: '%.2f' % (x, )
            )
        )


def test_whole_fmf(lstream):
    lstream.inject_packets(
        [
            Header(),

            ReferenceSectionHeader(),
            Title('Title'),
            Creator('Creator'),
            Created('Timestamp'),
            Place('Place'),

            MetaSectionHeader('My Section'),
            KeyValue('x', '1.3'),
            KeyValue('important parameter', r'\eta = 1.24e-9 mW'),

            TableDefinitionsHeader(),
            KeyValue('table1', 't_1'),
            KeyValue('table2', 't_2'),

            DataDefinitionsHeader('t_1'),
            KeyValue('distance', 'd [m]'),
            KeyValue('time', 't [s]'),

            DataHeader('t_1'),
            Comment('d    t'),
            DataRow(("2.3", "4.555")),
            DataRow(("1.2", "4.15")),

            DataDefinitionsHeader('t_2'),
            KeyValue('Energy', 'E [J]'),
            KeyValue('distance', 'd [m]'),

            DataHeader('t_2')
            ]
        )
    lstream.inject_packets(
        columns2rows(
            (
                DataColumn(("1.2", "1.3", "1.5", "1.6")),
                DataColumn(("2.2", "2.3", "2.5", "2.6"))
                )
            ) + [END_FMF]
        )


if __name__ == '__main__':
    pytest.main([__file__])
