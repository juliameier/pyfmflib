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


def test_basic_usage():
    class FooContext(object):
        def __init__(self):
            self.count = 0

    class FooProtocol(object):
        @staticmethod
        def verify_packet(packet, context):
            assert packet.find('in foo speak') > -1
            num = int(packet[-1])
            if num == 1:
                context.count = num
            else:
                assert num > context.count
            context.count = num

        @staticmethod
        def new_context(stream):
            return FooContext()

    class BarProtocol(streamlib.StaticProtocol):
        pass

    class Bar2Foo(streamlib.Adapter):
        input_protocol = BarProtocol
        output_protocol = FooProtocol

        def adapt_packet(self, packet, context):
            return ('Bar2Foo translation (now in foo speak) of ' + packet, )

    def new_default_foo_agent():
        agent = streamlib.Agent()
        agent.register_adapter(Bar2Foo())
        return agent

    class MySource(streamlib.Source):
        def inject_into(self, stream):
            inject = stream.inject_packet
            stream.set_protocol(FooProtocol)
            inject('stuff in foo speak 1')
            inject('stuff in foo speak 2')
            stream.set_protocol(BarProtocol)
            inject('stuff in bar speak 3')

            class BazProtocol(streamlib.StaticProtocol):
                pass

            class Baz2Foo(streamlib.Adapter):
                input_protocol = BazProtocol
                output_protocol = FooProtocol

                def adapt_packet(self, packet, context):
                    # return an iterable of adapted packets
                    return (
                        'Baz2Foo translation (now in foo speak) of ' + packet,
                        )

            baz2foo = Baz2Foo()
            stream.agent.register_adapter(baz2foo)
            stream.set_protocol(BazProtocol)
            inject('stuff in baz speak 4')
            stream.agent.unregister_adapter(baz2foo)
            stream.set_protocol(FooProtocol)
            inject('stuff in foo speak 5')

    class MyDestination(streamlib.Destination):
        protocol = FooProtocol

        def __init__(self):
            streamlib.Destination.__init__(self)
            self.packets = []

        def receive_packet(self, packet, context):
            self.packets.append(packet)

    # stream some stuff
    agent = new_default_foo_agent()  # has adapter foo -> bar by default
    source = MySource()
    destination = MyDestination()
    agent.transmit(source, destination)  # implicitly creates new tmp stream

    # stream some more stuff to the same destination,
    # recycling agent with bar -> foo adapter
    # and also recycling a stream
    source1 = MySource()
    source2 = MySource()
    stream = agent.new_stream(destination)
    source1.inject_into(stream)
    # or alternatively
    source2.inject_into(stream)

    expected_packets = [
        'stuff in foo speak 1',
        'stuff in foo speak 2',
        'Bar2Foo translation (now in foo speak) of stuff in bar speak 3',
        'Baz2Foo translation (now in foo speak) of stuff in baz speak 4',
        'stuff in foo speak 5'
        ] * 3
    assert destination.packets == expected_packets
