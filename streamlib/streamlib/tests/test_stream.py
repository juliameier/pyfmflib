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


class Protocol1(streamlib.StaticProtocol):
    pass


class Protocol2(streamlib.StaticProtocol):
    pass


class BufferedDestination(streamlib.Destination):
    protocol = Protocol1

    def __init__(self):
        streamlib.Destination.__init__(self)
        self.buffer = []

    def receive_packet(self, packet, context):
        self.buffer.append(packet)


@pytest.fixture
def plain_stream():
    agent = streamlib.Agent()
    stream = agent.new_stream(BufferedDestination())
    stream.set_protocol(stream.destination.protocol)
    return stream


def test_inject_packet(plain_stream):
    plain_stream.inject_packet(1)
    plain_stream.inject_packet("2")
    plain_stream.inject_packet(3.0)
    assert plain_stream.destination.buffer == [1, "2", 3.0]


def test_inject_packets(plain_stream):
    plain_stream.inject_packets((1, "2", 3.0))
    assert plain_stream.destination.buffer == [1, "2", 3.0]


# incomplete:
#def test_translation(plain_stream):
#    plain_stream.agent.register_adapter(...)
