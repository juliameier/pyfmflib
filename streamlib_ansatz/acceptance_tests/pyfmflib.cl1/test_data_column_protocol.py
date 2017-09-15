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
from fixtures import lhrstream


def test_inject_columns(lhrstream):
    from pyfmflib.cl1 import (
        DataColumn, FLUSH_DATA_COLUMNS, format_data_column,
        DataDefinitionsHeader, KeyValue, DataHeader, Comment
        )
    # we are still in line based protocol
    lhrstream.inject_packets(
        [
            DataDefinitionsHeader(),
            KeyValue('distance', 'd [m]'),
            KeyValue('time', 't [s]'),
            DataHeader(),
            Comment('d    t'),
            ]
        )

    # we can also use a formatter for columns
    fmt = lambda x: '%.2f' % (x, )

    lhrstream.set_protocol(cl1.DATA_COLUMN_PROTOCOL)
    lhrstream.inject_packets(
        [
            DataColumn(("1.2", "1.3", "1.5", "1.6")),
            format_data_column((2.2, 2.3, 2.5, 2.6), fmt),
    # FLUSH_DATA_COLUMNS is a special packet that triggers translation to
    # rows in the according adapter for all previously accumulated columns
            FLUSH_DATA_COLUMNS,
            DataColumn(("3.2", )),
            DataColumn(("5.1", )),
            FLUSH_DATA_COLUMNS
            ]
        )
    # don't forget to reset protocol
    lhrstream.set_protocol(cl1.LINE_BASED_PROTOCOL)


if __name__ == '__main__':
    pytest.main([__file__])
