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


class Meta_section(object):

    def __init__(self,name):
        self.name = name
        self.entries = []
        self.comments = []

    def initialize(*args):
        print args
        return Meta_section(name=None, entries=[], comments=[])

    def add_entry(self, key, value):

        for item in self.entries:
            if item.key == key:
                raise Exception('Key already exists')


        entry = Meta_section_entry(key, value)

        self.entries.append(entry)

        print len(self.entries)

        return entry

    def get_entry(self, key):
        print('key is:' , key)

        if key is not None:
            if self.entries is not None:
                for entry in self.entries:
                    if entry.key == key:
                        print ('key found')
                        return entry

                    else:
                        raise Exception('Key does not exist')

        else:
            if self.entries is not None:
                if len(self.entries) == 0:
                    raise Exception('No entries exist')


class Meta_section_entry:

    def __init__(self, key, value):

        self.key = key
        self.value = value


    def initialize(*args, **kwargs):

        print(args)
        print(kwargs)

        return Meta_section_entry(key=None, value=None)
