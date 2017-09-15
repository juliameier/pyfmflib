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
from pyfmflib.cl1 import (
    TableDefinitions, DataDefinitions, Data, KeyValue, Comment,
    DataRow, DataColumn, columns2rows, rowmajor2rows, columnmajor2rows
    )


def test_create_table_definitions():
    TableDefinitions(
        [
            Comment('just to illustrate'),
            KeyValue('time distance measurement 1', 'TDM_1')
            ]
        )


def test_create_data_definitions():
    DataDefinitions(
        symbol='TDM_1',
        entries=[
            KeyValue('time', 't [s]'),
            KeyValue('distance', 's(t) [m]'),
            Comment('useless comment')
            ]
        )


def test_create_anonymous_data_definitions():
    DataDefinitions(
        symbol=None,  # default value, just to illustrate
        entries=[KeyValue('time', 't [s]')]
        )


def test_create_data():
    # DataRow accepts any iterable with string elements
    Data(
        symbol='TDM_1',
        entries=[
            Comment('t / s    s(t) / m'),
            DataRow(('0', '-2')),
            DataRow(['1.1', '0.1']),
            DataRow(set(('2.0', '3.1'))),
            DataRow(iter(('2.9', '4.5'))),
            ]
        )


def test_create_data_from_columns():
    # DataColumn accepts any iterable with string elements
    Data(
        symbol='TDM_1',
        entries=[
            Comment('t / s    s(t) / m'),
            Comment('here be columns'),
            ] + columns2rows(
            (
                DataColumn(('0', '1.1', '2.0', '2.9')),
                DataColumn(('-2', '0.1', '3.1', '4.5'))
                )
            ) + [
            Comment('here be rows'),
            DataRow(('3.2', '6.7'))  # we can mix rows and columns
            ]
        )


def test_create_data_from_nested_iterable():
    Data(
        symbol='TDM_1',
        entries=[
            Comment('t / s    s(t) / m'),
            Comment('here be data'),
            ] + rowmajor2rows(  # row major order "C-style"
            (
                ('0', '-2'),
                ('1.1', '0.1'),
                ('2.0', '3.1'),
                ('2.9', '4.5')
                )
            ) + columnmajor2rows(  # column major order "Fortran-style"
            (
                ('0', '1.1', '2.0', '2.9'),
                ('-2', '0.1', '3.1', '4.5')
                )
            )
        )


def test_create_data_from_custom_source():
    # formatter is called for every cell, replacing the cell
    # formatter also available for:
    # columnmajor2rows, DataRow and DataColumn
    #
    # for more elaborate examples see test_streaming
    Data(
        symbol='TDM_1',
        entries=[
            Comment('t / s    s(t) / m'),
            Comment('here be data from custom source')
            ] + rowmajor2rows(
            (
                (0, -2),
                (1.1, 0.1),
                (2.0, 3.1),
                (2.9, 4.5)
                ),
            formatter=lambda x: '%.1f' % (x, )
            ),
        )


def test_create_anonymous_data():
    Data(
        symbol=None,  # default value, just to illustrate
        entries=[DataRow(('1.', )), DataRow(('2.', ))]
        )


if __name__ == '__main__':
    pytest.main([__file__])
