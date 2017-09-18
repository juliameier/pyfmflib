#! /usr/bin/env python
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


from pyfmflib.meta_section import Meta_section, Meta_section_entry
from pyfmflib.fmf import FMF

class Test_Meta_Section:

    def setup(self):
        self.meta_section = Meta_section('Meta Section Name')

    def test_create_meta_section(self):
        assert self.meta_section is not None

    def test_meta_section_object(self):
        assert isinstance(self.meta_section, Meta_section)

    def test_add_meta_section_to_fmf(self):
        fmf_object = FMF()

        fmf_object.meta_sections = [fmf_object.add_meta_section(self.meta_section.name)]

        assert fmf_object.meta_sections is not None

    def test_add_entry(self):
        entry = Meta_section.add_entry(self.meta_section,'key','value')

        assert entry is not None

        self.meta_section.entries.append(entry)

        assert len(self.meta_section.entries) > 0

    def test_add_entry_with_same_name(self):
#        entry1 = Meta_section.add_entry(self.meta_section,'key1','value1')
#        entry2 = Meta_section.add_entry(self.meta_section,'key1','value2')

        entry1 = Meta_section_entry('key1','value1')
        entry2 = Meta_section_entry('key2','value2')

        assert entry1.key != entry2.key


    def test_get_entry(self):

        key = 'key1'
        value = 'value1'
        entry1 = Meta_section.add_entry(self.meta_section, key, value)

        item = Meta_section.get_entry(self.meta_section, key)

        print (item.value)
        print (self.meta_section.name)

        assert item is not None

        assert item.key == key and item.value == value


    def test_get_entry_wrong_key(self):
        key = 'key1'
        value = 'value1'
        entry1 = Meta_section.add_entry(self.meta_section, key, value)

        self.meta_section.entries.append(entry1)

        key_to_get = 'key2'

        item_key = self.meta_section.entries.__getitem__(0).key

        assert key_to_get == item_key


    def test_get_entry_no_entries(self):
        item = Meta_section.get_entry(self.meta_section, None)






