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
import streamlib
from pyfmflib.cl1 import (
    Header, ReferenceSectionHeader, Title, Creator, Created, Place,
    MetaSectionHeader, KeyValue, TableDefinitionsHeader,
    DataDefinitionsHeader, DataHeader, Comment, DataRow, DataColumn,
    columns2rows, END_FMF
    )


@pytest.fixture
def empty_fmf():
    return cl1.new_empty_fmf()


@pytest.fixture
def fmf_template():
    return cl1.new_fmf_template()


@pytest.fixture
def meta_section():
    return cl1.MetaSection(
        identifier='A Meta Section',
        entries=[
            cl1.Comment('a comment'),
            cl1.KeyValue('key', 'value'),
            cl1.KeyValue('another key', 'another value'),
            cl1.Comment('another comment')
            ]
        )


@pytest.fixture
def fmf_template_with_tables():
    from pyfmflib.cl1 import (
        TableDefinitions, DataDefinitions, Data, KeyValue, DataRow, Comment
        )
    fmf = cl1.new_fmf_template()
    fmf.table_sections = [
        TableDefinitions(
            [
                Comment('A comment'),
                KeyValue('Table 1', 't_1'),
                KeyValue('Table 2', 't_2'),
                ]
            ),
        DataDefinitions(
            symbol='t_1',
            entries=[
                KeyValue('time', 't [s]'),
                Comment('Another comment'),
                KeyValue('distance', 's(t) [m]'),
                ]
        ),
        Data(
            symbol='t_1',
            entries=[
                DataRow(('0', '-2')),
                DataRow(('1.1', '0.1')),
                DataRow(('2.0', '3.1')),
                Comment('Yet another comment'),
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
    return fmf


def prepare_stream(protocol):
    agent = cl1.new_default_agent()
    _prtcl = protocol

    class NoOpDestination(streamlib.Destination):
        protocol = _prtcl
        receive_packet = lambda self, packet, context: None

    stream = agent.new_stream(NoOpDestination())
    stream.set_protocol(protocol)
    return stream


@pytest.fixture
def lstream():
    return prepare_stream(cl1.LINE_BASED_PROTOCOL)


@pytest.fixture
def lhstream():
    stream = prepare_stream(cl1.LINE_BASED_PROTOCOL)
    stream.inject_packet(cl1.Header())
    return stream


@pytest.fixture
def lhrstream():
    stream = prepare_stream(cl1.LINE_BASED_PROTOCOL)
    stream.inject_packets(
        [
            cl1.Header(),
            cl1.SectionHeader('*reference'),
            cl1.Title('Title'),
            cl1.Creator('Creator'),
            cl1.Created('Created'),
            cl1.Place('Place'),
            ]
        )
    return stream


@pytest.fixture
def lsource():
    class LineOnlySource(streamlib.Source):
        def inject_into(self, stream):
            stream.set_protocol(cl1.LINE_BASED_PROTOCOL)
            stream.inject_packets(
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
                    DataHeader('t_2'),
                    ] + columns2rows(
                    (
                        DataColumn(("1.2", "1.3", "1.5", "1.6")),
                        DataColumn(("2.2", "2.3", "2.5", "2.6")),
                        )
                    ) + [END_FMF]
                )
    return LineOnlySource()


@pytest.fixture
def agent():
    return cl1.new_default_agent()
