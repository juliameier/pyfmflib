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
from pyfmflib.cl1 import MetaSection, Comment, KeyValue, Comment
from fixtures import meta_section


def test_create_meta_section():
    MetaSection(
        identifier='my metadata section',
        entries=[
            Comment('this is a metadata section'),
            KeyValue('important parameter', '\Gamma = 0.137e-12 J/K'),
            Comment('useless comment'),
            KeyValue('x', '2'),
            Comment('All but global comments that occur'),
            Comment('before the first section belong to a section.')
            ]
        )


def test_append_to_meta_section_by_key(meta_section):
    # this should append at the end of the section
    old_len = len(meta_section.entries)
    meta_section['an unused key'] = 'a new value'
    assert len(meta_section.entries) == old_len + 1
    assert meta_section.entries[-1] == KeyValue('an unused key', 'a new value')


def test_insert_comment_into_meta_section(meta_section):
    meta_section.entries.insert(
        2,
        Comment('A comment between the key value entries')
        )


def test_get_meta_section_value_by_key(meta_section):
    assert meta_section['another key'] == 'another value'


def test_replace_meta_section_value_by_key(meta_section):
    # this should preserve the order
    meta_section['key'] = 'replaced value'
    assert meta_section.entries[1].value == 'replaced value'


def test_equality():
    assert MetaSection(
        identifier='foo', entries=[KeyValue('1', '2'), Comment('bar')]
        ) == MetaSection(
        identifier='foo', entries=[KeyValue('1', '2'), Comment('bar')]
        )


if __name__ == '__main__':
    pytest.main([__file__])
