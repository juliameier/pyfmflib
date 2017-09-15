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
import streamlib
from pyfmflib import cl1
from fixtures import lsource, fmf_template_with_tables, agent
from pyfmflib.cl1 import (
    Header, ReferenceSectionHeader, Title, Creator, Created, Place,
    DataDefinitionsHeader, KeyValue, DataHeader, Comment, DataRow, END_FMF,
    MetaSectionHeader, TableDefinitionsHeader, inject_columns, DataColumn
    )


def test_implement_a_source():
    class MySource(streamlib.Source):
        def inject_into(self, stream):
            # also see test_line_protocol.py
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

                    DataHeader('t_2')
                    ]
                )

            inject_columns(
                stream,
                (
                    DataColumn(("1.2", "1.3", "1.5", "1.6")),
                    DataColumn(("2.2", "2.3", "2.5", "2.6"))
                    )
                )

            stream.inject_packet(END_FMF)


def test_stream_source_to_textfile_explicit(lsource):
    agent = cl1.new_default_agent()
    with open('mydata.fmf', 'w') as handle:
        # a cl1.FileLikeDestination simply writes all received packets
        # to a given file like object (handle)
        dest = cl1.FileLikeDestination(handle)
        agent.transmit(lsource, dest)


def test_stream_source_to_textfile_explicit_alternative(lsource):
    agent = cl1.new_default_agent()
    with open('mydata.fmf', 'w') as handle:
        dest = cl1.FileLikeDestination(handle)
        stream = agent.new_stream(dest)
        lsource.inject_into(stream)


def test_stream_source_to_textfile_convenient(lsource):
    cl1.write(lsource, 'mydata.fmf')


def test_stream_custom_protocol_to_textfile(agent):
    import numpy as np

    class MyNumpyProtocol(streamlib.StaticProtocol):
        # do not actually verify anything, since this protocol
        # is not going to be used in a destination
        pass

    # Custom adapter from custom protocol (numpy arrays)
    # to line based protocol.
    # This use case might better be covered by a higher level protocol
    # in the future, when it is possible to send a Data instance.
    # reminder: find a more useful example besides numpy arrays
    class MyNumpyAdapter(streamlib.Adapter):
        input_protocol = MyNumpyProtocol
        output_protocol = cl1.LINE_BASED_PROTOCOL

        def adapt_packet(self, packet, context):
            # rowmajor2rows works with any nested iterable
            # see also test_table_sections.py
            return cl1.rowmajor2rows(packet)

    class MySource(streamlib.Source):
        def inject_into(self, stream):
            stream.set_protocol(cl1.LINE_BASED_PROTOCOL)

            stream.inject_packets(
                [
                    Header(delimiter='whitespace'),

                    ReferenceSectionHeader(),
                    Title('Title'),
                    Creator('Creator'),
                    Created('Timestamp'),
                    Place('Place'),

                    DataDefinitionsHeader(),
                    KeyValue('distance', 'd [m]'),
                    KeyValue('time', 't [s]'),

                    DataHeader(),
                    Comment('custom formatter test:'),
                    Comment('d    t')
                    ]
                )
            # going to stream in custom protocol
            # the agent will find and use any registered adapters
            stream.set_protocol(MyNumpyProtocol)
            stream.inject_packet(np.random.uniform(size=(10, 2)))
            stream.inject_packet(np.random.uniform(size=(5, 2)))
            # going to stream in line based protocol again
            stream.set_protocol(cl1.LINE_BASED_PROTOCOL)
            stream.inject_packet(DataRow(("2.3", "4.555")))
            stream.inject_packet(DataRow(["1.2", "4.15"]))

            stream.inject_packet(END_FMF)

    agent.register_adapter(MyNumpyAdapter())
    source = MySource()
    with open('mydata.fmf', 'w') as handle:
        dest = cl1.FileLikeDestination(handle)
        agent.transmit(source, dest)

    # alternatively
    cl1.write(
        source, 'mydata.fmf',
        adapters=[MyNumpyAdapter()]
        )


def test_stream_stuff_to_fmf_instance(lsource, agent):
    my_fmf_instance = cl1.new_empty_fmf()
    # every fmf instance is a LineBasedDestination accepting
    # the cl1.LINE_BASED_PROTOCOL
    agent.transmit(lsource, my_fmf_instance)


def test_stream_fmf_instance_to_file(fmf_template_with_tables):
    # every fmf instance is also a streamlib.Source speaking
    # in protocols that cl1 knows how to translate them
    # to text
    cl1.write(fmf_template_with_tables, 'mydata.fmf')


def test_stream_fmf_instance_to_custom_destination(
    fmf_template_with_tables, agent
    ):
    class CommentPrinter(streamlib.Destination):
        protocol = cl1.LINE_BASED_PROTOCOL

        def receive_packet(self, packet, context):
            if isinstance(packet, cl1.Comment):
                print packet

    # or provide fancy line based Destination, like so:
    class CommentPrinter2(cl1.LineBasedDestination):
        def receive_comment(self, comment, context):
            print comment

    agent.transmit(fmf_template_with_tables, CommentPrinter())
    agent.transmit(fmf_template_with_tables, CommentPrinter2())


# should this test be moved to CL3 later?
def test_stream_fmf_instance_to_another_compliance_level(
    fmf_template_with_tables
    ):
    cl1_fmf = fmf_template_with_tables

    # we need a cl3 agent here that knows how to translate
    # from CL1 to CL3 protocol
    cl3 = pytest.importorskip("pyfmflib.cl3")
    cl3_agent = cl3.new_default_agent()
    # transmit returns the destination
    cl3_fmf = cl3_agent.transmit(cl1_fmf, cl3.FMF())

    # and back ...
    cl1_fmf_inconvenient_copy = cl3_agent.transmit(cl3_fmf, cl1.FMF())
    assert cl1_fmf_inconvenient_copy == cl1_fmf  # do we implement == ?


if __name__ == '__main__':
    pytest.main([__file__])
