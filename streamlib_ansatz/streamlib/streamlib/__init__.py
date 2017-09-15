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
@package streamlib
The streamlib package

Basic usage methodology:

agent = SomeAgent()
source = SomeSource()
destination = SomeDestination()

# transmit:
stream = agent.new_stream()
source.inject_into(stream)
# or
agent.transmit(source, destination)
"""


class Protocol(object):
    """
    A protocol verifies packets.

    Be aware that only packets in the destination protocol
    of a stream are verified by the framework
    (e.g. after translation through an adapter)!
    """

    def verify_packet(self, packet, context):
        """Raises an exception iff the packet does not obey the protocol."""
        pass

    def new_context(self, stream):
        """
        Returns a context for the given stream.

        This context will be passed to self.verify_packet later.
        """
        return None


class StaticProtocol(object):
    """Static version of Protocol for convenience."""

    @staticmethod
    def verify_packet(packet, context):
        pass

    @staticmethod
    def new_context(stream):
        return None


class Source(object):
    """A source that sends packets in any protocol."""

    def inject_into(self, stream):
        """
        Injects packets into a stream

        by repeatedly calling stream.inject_packet(packet)
        or stream.inject_packets(packets).
        Changes/Sets the protocol by calling stream.set_protocol(protocol)
        """
        raise NotImplementedError


class Destination(object):
    """A destination that receives packets in a given protocol."""

    protocol = NotImplemented

    def receive_packet(self, packet, context):
        """
        Receives a packet in a given context

        Does something useful with the packet
        possibly using additional information from the context.
        """
        raise NotImplementedError

    def new_context(self, stream):
        """
        Returns a context for the given stream.

        This context will be passed to self.receive_packet later.
        """
        return None


class Adapter(object):
    """An adapter that translates packets from one protocol to another."""

    input_protocol = NotImplemented
    output_protocol = NotImplemented

    def adapt_packet(self, packet, context):
        """
        Translates packets from input_protocol to output_protocol.

        Returns an iterable of packets in the output_protocol.
        May read or write state from/to the context, e.g. in order
        to delay translation until all necessary information is available.
        The adapter itself is stateless, since it has to be able to handle
        any number of streams.
        """
        raise NotImplementedError

    def new_context(self, stream):
        """
        Returns a context for the given stream.

        This context will be passed to self.adapt_packet later.
        """
        return None


class Stream(object):
    """A stream is an agent providing adapters together with a destination."""

    def __init__(self, agent, destination):
        self.agent = agent
        self.destination = destination
        self.current_protocol = None
        self.current_adapter = None
        self.protocol_context = destination.protocol.new_context(self)
        self.destination_context = destination.new_context(self)
        self.current_adapter_context = None
        self.adapter_contexts = {}

    def inject_packet(self, packet):
        """
        Injects a packet into the stream

        The packet is translated using adapters from self.agent
        if necessary. The (translated) packet(s) are then verified
        by the protocol and send to self.destination.
        """
        if self.current_protocol is None:
            raise ValueError('Protocol not set!')
        if self.current_adapter is None:
            self._send_destination_packet(packet)
        else:
            for packet in self.current_adapter.adapt_packet(
                packet, self.current_adapter_context
                ):
                self._send_destination_packet(packet)

    def inject_packets(self, packets):
        """
        Injects packets into the stream

        The packets are translated using adapters from self.agent
        if necessary. The (translated) packet(s) are then verified
        by the protocol and send to self.destination.
        """
        for packet in packets:
            self.inject_packet(packet)

    def set_protocol(self, protocol):
        """Sets the current protocol of the stream."""
        if protocol == self.current_protocol:
            return
        self.current_protocol = protocol
        if protocol == self.destination.protocol:
            self.current_adapter = None
            self.current_adapter_context = None
        else:
            self.current_adapter = self.agent.find_adapter(
                protocol, self.destination.protocol
                )
            try:
                adpt_context = self.adapter_contexts[self.current_adapter]
            except KeyError:
                adpt_context = self.current_adapter.new_context(self)
                self.adapter_contexts[self.current_adapter] = adpt_context
            self.current_adapter_context = adpt_context

    def _send_destination_packet(self, packet):
        self.destination.protocol.verify_packet(packet, self.protocol_context)
        self.destination.receive_packet(packet, self.destination_context)


class Agent(object):
    """An agent is a registry for adapters and a stream factory."""

    def __init__(self):
        self._adapters = {}

    def register_adapter(self, adapter):
        """
        Registers an adapter.

        This implementation does not check for duplicates.
        """
        key = (adapter.input_protocol, adapter.output_protocol)
        alist = self._adapters.get(key, None)
        if alist is None:
            alist = []
            self._adapters[key] = alist
        alist.append(adapter)

    def unregister_adapter(self, adapter):
        """Unregisters an adapter."""
        key = (adapter.input_protocol, adapter.output_protocol)
        alist = self._adapters.get(key, [])
        alist.remove(adapter)

    def find_adapter(self, input_protocol, output_protocol):
        """Returns an adapter matching the I/O protocols."""
        key = (input_protocol, output_protocol)
        return self._adapters[key][-1]

    def transmit(self, source, destination):
        """
        Transmits from source to destination

        creating a temporary stream with self.new_stream(destination).
        Returns destination.
        """
        source.inject_into(self.new_stream(destination))
        return destination

    def new_stream(self, destination):
        """Returns a Stream instance."""
        return Stream(agent=self, destination=destination)
