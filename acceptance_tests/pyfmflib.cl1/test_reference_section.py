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


def test_create_minimal_reference_section():
    cl1.new_minimal_reference_section(
        creator='Creator',
        created='Timestamp',
        title='Title',
        place='Place'
        )


def test_create_custom_reference_section():
    # cl1.Title is short for cl1.KeyValue('Title', ...) etc.
    cl1.ReferenceSection(
        [
            cl1.Comment(
                'We can control exactly, where to put comments!'
                ),
            cl1.Creator('Creator'),
            cl1.Created('Timestamp'),
            cl1.Comment('a comment in between'),
            cl1.Title('Title'),
            cl1.Place('Place'),
            cl1.Comment('and a comment at the end')
            ]
        )


def test_equality():
    assert cl1.new_minimal_reference_section(
        creator='Creator',
        created='Timestamp',
        title='Title',
        place='Place'
        ) == cl1.new_minimal_reference_section(
        creator='Creator',
        created='Timestamp',
        title='Title',
        place='Place'
        )


if __name__ == "__main__":
    pytest.main([__file__])
