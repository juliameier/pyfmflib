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


from pyfmflib.meta_section import Meta_section
from pyfmflib.reference_section import Reference_section
from pyfmflib.table import Table

class FMF:
    def __init__(self):

            self.header = None
            self.reference_section = None
            self.meta_sections = []
            self.table_sections = []
            self.global_comments = []
            self.compliance_level = None


    def initialize(*args, **kwargs):

        # args represents the regular arguments
        # kwargs represents the keyword arguments
        print args, kwargs
        print (len(args))
        print (len(kwargs))

        return FMF(header=None, meta_sections=[], tables=[], global_comments=[], compliance_level=None)


    def set_reference(self, title, creator, place, created, contact):
        self.reference_section = Reference_section(title, creator, created, place, contact)

        return self.reference_section


    def add_table(self, name, symbol):

        table = Table(name, symbol)

        return table

    def add_meta_section(self,name):

        if self.meta_sections is not None:
            for item in self.meta_sections:
                if item.name == name:
                    raise Exception('Meta section with this name already exists')

        if name.find("*") != -1:
            raise Exception(" '*' is not allowed as first character")

        meta_section = Meta_section(name)

#        self.meta_sections.append(meta_section)

        return meta_section

    def get_meta_section(self, name):
        if self.meta_sections is not None:
            for item in self.meta_sections:
                if item.name == name:
                    print ('Meta section found')
                    return item

                else:
                    raise Exception('Meta section with specified name does not exist')
