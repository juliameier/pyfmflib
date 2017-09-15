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

"""
cl1fmflib skeleton as defined through acceptance tests

TODO: move this stuff out of __init__.py and split it into
      separate modules for the actual fleshing out
"""

import streamlib


class Header(object):
    def __init__(
        self,
        coding='utf-8',
        fmfversion='1.1',
        comment_char=';',
        delimiter='tab',
        extra_parameters=None
        ):
        self.coding = coding
        self.fmfversion = fmfversion
        self.comment_char = comment_char
        self.delimiter = delimiter
        if extra_parameters is None:
            extra_parameters = {}
        self.extra_parameters = extra_parameters

    @property
    def delimiter_char(self):
        # todo: complete dict
        return {
            'tab': '\t',
            }[self.delimiter]

    def __eq__(self, other):
        if not isinstance(other, Header):
            return NotImplemented
        return self.coding == other.coding and \
            self.fmfversion == other.fmfversion and \
            self.comment_char == other.comment_char and \
            self.delimiter == other.delimiter and \
            self.extra_parameters == other.extra_parameters

    def __ne__(self, other):
        value = self.__eq__(other)
        if value == NotImplemented:
            return value
        return not value


class Comment(str):
    pass


class SectionHeader(object):
    def __init__(self, identifier):
        self.identifier = identifier

    def __eq__(self, other):
        if not isinstance(other, SectionHeader):
            return NotImplemented
        return self.identifier == other.identifier

    def __ne__(self, other):
        value = self.__eq__(other)
        if value == NotImplemented:
            return value
        return not value


class DataDefinitionsHeader(SectionHeader):
    def __init__(self, symbol=None):
        identifier = '*data definitions'
        if symbol is not None:
            identifier += ': ' + symbol
        SectionHeader.__init__(self, identifier)


class DataHeader(SectionHeader):
    def __init__(self, symbol=None):
        identifier = '*data'
        if symbol is not None:
            identifier += ': ' + symbol
        SectionHeader.__init__(self, identifier)


class ReferenceSectionHeader(SectionHeader):
    def __init__(self):
        SectionHeader.__init__(self, '*reference')


class MetaSectionHeader(SectionHeader):
    pass


class TableDefinitionsHeader(SectionHeader):
    def __init__(self):
        SectionHeader.__init__(self, '*table definitions')


class Section(object):
    def __init__(self, identifier, entries=None):
        self.identifier = identifier
        if entries is None:
            entries = []
        self.entries = entries

    def __eq__(self, other):
        if not isinstance(other, Section):
            return NotImplemented
        return self.identifier == other.identifier and \
            self.entries == other.entries

    def __ne__(self, other):
        value = self.__eq__(other)
        if value == NotImplemented:
            return value
        return not value


class KeyValueSection(Section):
    def __getitem__(self, key):
        # change implementation?
        for entry in self.entries:
            if isinstance(entry, KeyValue):
                if entry.key == key:
                    return entry.value
        raise KeyError(key)

    def __setitem__(self, key, value):
        # change implementation?
        for entry in self.entries:
            if isinstance(entry, KeyValue):
                if entry.key == key:
                    entry.value = value
                    return
        self.entries.append(KeyValue(key, value))


class MetaSection(KeyValueSection):
    pass


class ReferenceSection(MetaSection):
    def __init__(self, entries):
        MetaSection.__init__(self, '*reference', entries)


class KeyValue(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, KeyValue):
            return NotImplemented
        return self.key == other.key and self.value == other.value

    def __ne__(self, other):
        value = self.__eq__(other)
        if value == NotImplemented:
            return value
        return not value


class FixedKeyValue(KeyValue):
    key = NotImplemented

    def __init__(self, value):
        KeyValue.__init__(self, self.key, value)


class Creator(FixedKeyValue):
    key = 'creator'


class Created(FixedKeyValue):
    key = 'created'


class Title(FixedKeyValue):
    key = 'title'


class Place(FixedKeyValue):
    key = 'place'


class TableDefinitions(KeyValueSection):
    def __init__(self, entries):
        KeyValueSection.__init__(self, '*table definitions', entries)


class DataDefinitions(KeyValueSection):
    def __init__(self, symbol=None, entries=None):
        identifier = '*data definitions'
        if symbol is not None:
            identifier += ': ' + symbol
        KeyValueSection.__init__(self, identifier, entries)


class Data(Section):
    def __init__(self, symbol=None, entries=None):
        identifier = '*data'
        if symbol is not None:
            identifier += ': ' + symbol
        Section.__init__(self, identifier, entries)


class DataRow(list):
    def __eq__(self, other):
        if not isinstance(other, DataRow):
            return False
        return list.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)


class DataColumn(list):
    def __eq__(self, other):
        if not isinstance(other, DataColumn):
            return False
        return list.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)


def columns2rows(columns):
    return [DataRow(row) for row in zip(*columns)]


def rowmajor2rows(nested_iterable, formatter=None):
    return [format_data_row(row, formatter) for row in nested_iterable]


def columnmajor2rows(nested_iterable, formatter=None):
    return [format_data_row(row, formatter) for row in zip(*nested_iterable)]


class LineBasedProtocol(streamlib.Protocol):
    pass


class DataColumnProtocol(streamlib.Protocol):
    pass


LINE_BASED_PROTOCOL = LineBasedProtocol()
DATA_COLUMN_PROTOCOL = DataColumnProtocol()


class DefaultAgent(streamlib.Agent):
    pass


class Column2LineAdapter(streamlib.Adapter):
    input_protocol = DATA_COLUMN_PROTOCOL
    output_protocol = LINE_BASED_PROTOCOL

    def adapt_packet(self, packet, context):
        return []


COLUMN_2_LINE_ADAPTER = Column2LineAdapter()


def new_default_agent():
    agent = DefaultAgent()
    agent.register_adapter(COLUMN_2_LINE_ADAPTER)
    return agent


def new_empty_fmf():
    return FMF(
        header=None,
        global_comments=[],
        meta_sections=[],
        table_sections=[]
        )


def new_fmf_template():
    return FMF(
        header=Header,
        global_comments=[],
        meta_sections=[
            new_minimal_reference_section(
                creator='Creator',
                created='Created',
                title='Title',
                place='Place'
                ),
            MetaSection(
                identifier='A Section',
                entries=[
                    KeyValue('key1', '"value1"'),
                    KeyValue('key2', '"value2"')
                    ]
                )
            ],
        table_sections=[]
        )


class LineBasedDestination(streamlib.Destination):
    protocol = LINE_BASED_PROTOCOL

    def receive_packet(self, packet, context):
        pass

    def receive_header(self, header, context):
        pass

    def receive_comment(self, comment, context):
        pass

    def receive_section_header(self, section_header, context):
        pass

    def receive_key_value(self, key_value, context):
        pass

    def receive_data_row(self, data_row, context):
        pass

    def receive_end_fmf(self, end_fmf, context):
        pass


class FMF(LineBasedDestination, streamlib.Source):
    protocol = LINE_BASED_PROTOCOL

    def __init__(
        self,
        header,
        global_comments,
        meta_sections,
        table_sections
        ):
        streamlib.Destination.__init__(self)
        streamlib.Source.__init__(self)
        self.header = header
        self.global_comments = global_comments
        self.meta_sections = meta_sections
        self.table_sections = table_sections

    def __getitem__(self, key):
        # change implementation?
        for ms in self.meta_sections:
            if ms.identifier == key:
                return ms
        raise KeyError(key)

    def __eq__(self, other):
        if not isinstance(other, FMF):
            return NotImplemented
        return self.header == other.header and \
            self.global_comments == other.global_comments and \
            self.meta_sections == other.meta_sections and \
            self.table_sections == other.table_sections

    def __ne__(self, other):
        value = self.__eq__(other)
        if value == NotImplemented:
            return value
        return not value

    def inject_into(self, stream):
        pass

    def receive_packet(self, packet, context):
        pass


def new_fmf_with_default_header():
    return FMF(
        header=Header(),
        global_comments=[],
        meta_sections=[],
        table_sections=[]
        )


class FlushDataColumnsPacket(object):
    pass


FLUSH_DATA_COLUMNS = FlushDataColumnsPacket()


def write(source, filename_or_filelike, adapters=None):
    pass


def new_minimal_fmf(title, creator, created, place):
    pass


def format_data_row(iterable, formatter):
    if formatter is None:
        return DataRow(iterable)
    else:
        return DataRow(map(formatter, iterable))


def format_data_column(iterable, formatter):
    if formatter is None:
        return DataColumn(iterable)
    else:
        return DataColumn(map(formatter, iterable))


def new_minimal_reference_section(creator, created, title, place):
    return ReferenceSection(
        entries=[
            Creator(creator),
            Created(created),
            Title(title),
            Place(place)
            ]
        )


def inject_columns(stream, columns):
    stream.inject_packets(
        columns2rows(columns)
        )


class EndFMFPacket(object):
    pass


END_FMF = EndFMFPacket()


class FileLikeDestination(LineBasedDestination):
    def __init__(self, handle):
        LineBasedDestination.__init__(self)
        self.handle = handle
