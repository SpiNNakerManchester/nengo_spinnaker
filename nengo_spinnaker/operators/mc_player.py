import collections
from rig.machine import Cores, SDRAM
import struct

from nengo_spinnaker.builder.builder import netlistspec
from nengo_spinnaker.netlist import Vertex
from nengo_spinnaker import regions
from nengo_spinnaker.utils.application import get_application


class MulticastPacketSender(Vertex):
    """Object which will send pre-specified multicast packets at the start and
    end of a simulation.
    """
    def __init__(self, start_packets=list(), end_packets=list()):
        super(MulticastPacketSender, self).__init__(get_application("mc_player"))
        
        # Store the lists of packets to send
        self.start_packets = list(start_packets)
        self.end_packets = list(end_packets)

    def make_vertices(self, model, n_steps):
        """Make a vertex for the operator."""
        # Construct the regions
        self.regions = [
            None,
            PacketRegion(self.start_packets),
            None,
            PacketRegion(self.end_packets)
        ]

        # Make the vertex
        self.resources[Cores] = 1
        self.resources[SDRAM] = regions.utils.sizeof_regions(self.regions,
                                                             slice(None))

        # Return the spec
        return netlistspec(self, self.load_to_machine)

    def load_to_machine(self, netlist, controller):
        """Load data to the machine."""
        # Get the memory
        region_mem = regions.utils.create_app_ptr_and_region_files(
            netlist.vertices_memory[self], self.regions, None)

        # Write the regions into memory
        for region, mem in zip(self.regions, region_mem):
            if region is not None:
                region.write_subregion_to_file(mem, slice(None))


class Packet(collections.namedtuple("Packet", "key, payload")):
    """Multicast Packet"""
    def __new__(cls, key, payload=None):
        return super(Packet, cls).__new__(cls, key, payload)


class PacketRegion(regions.Region):
    def __init__(self, packets):
        # Store the packets
        self.packets = packets

    def sizeof(self, *args, **kwargs):
        # 1 word plus 4 words per packet
        return 4*(1 + len(self.packets))

    def write_subregion_to_file(self, fp, *args, **kwargs):
        # Write 1 word for the number of packets and then 4 words per packet.
        # Buffer the data locally
        data = struct.pack("<I", len(self.packets))

        for packet in self.packets:
            print packet.key.get_value()
            data += struct.pack("<4I", 0x0, packet.key.get_value(), packet.payload or 0x0,
                                0x0 if packet.payload is None else 0x1)
        print ",".join("{:02x}".format(ord(b)) for b in data)
        # Write the data to file
        fp.write(data)