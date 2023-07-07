from io import BytesIO
from struct import unpack
import os

import numpy as np

from .binary_data import BinaryData
from .crc import CRC

class Package:
    def __init__(self):
        self.ProtocolVersion: np.uint8
        self.SecurityKeyID: np.uint8
        self.Prefix: str
        self.Route: str
        self.EncryptionAlg: str
        self.Compression: str
        self.Priority: str
        self.HeaderLength: np.uint8
        self.HeaderEncoding: np.uint8
        self.FrameDataLength: np.uint16
        self.PacketIdentifier: np.uint16
        self.PacketType: np.uint8
        self.PeerAddress: np.uint16
        self.RecipientAddress: np.uint16
        self.TimeToLive: np.uint8
        self.HeaderCheckSum: np.uint8
        self.ServicesFrameData: BinaryData
        self.ServicesFrameDataCheckSum: np.uint16

    def decode(self, content, options=None):
        """Decode buff to package structure"""
        buf = BytesIO(content)
        p = self
        p.ProtocolVersion: np.uint8 = unpack('<B', buf.read(1))[0]
        p.SecurityKeyID: np.uint8 = unpack('<B', buf.read(1))[0]

        # parse flags
        flags = unpack('<B', buf.read(1))[0]
        flag_bits = f"{flags:08b}"
        p.Prefix = flag_bits[:2]
        p.Route = flag_bits[2:3]
        p.EncryptionAlg = flag_bits[3:5]
        p.Compression = flag_bits[5:6]
        p.Priority = flag_bits[6:]

        p.HeaderLength = unpack('<B', buf.read(1))[0]
        p.HeaderEncoding = unpack('<B', buf.read(1))[0]
        p.FrameDataLength = unpack('<H', buf.read(2))[0]
        p.PacketIdentifier = unpack('<H', buf.read(2))[0]
        p.PacketType = unpack('<B', buf.read(1))[0]

        if p.Route == "1":
            p.PeerAddress = unpack('<H', buf.read(2))[0]
            p.RecipientAddress = unpack('<H', buf.read(2))[0]
            p.TimeToLive = unpack('<B', buf.read(1))[0]

        p.HeaderCheckSum = unpack('<B', buf.read(1))[0]

        if p.HeaderCheckSum == CRC.crc8(content[:p.HeaderLength-1]):
            print("Valid Header checksum!")
        else:
            raise Exception("Wrond checksum of Header")
        
        ##########################################################
        
        # Here sould be working with inner structures and secret
        
        ##########################################################

        buf.seek(-2, os.SEEK_END) # makes new position to read buff from end -2 bytes
        p.ServicesFrameDataCheckSum = unpack('<H', buf.read(2))[0]
        if p.ServicesFrameDataCheckSum == CRC.crc16(content[p.HeaderLength:p.HeaderLength+p.FrameDataLength]):
            print("Valid ServicesFrameData checksum!")
        else:
            raise Exception("Wrond ServicesFrameData checksum")
        
    def print_packet_values(self) -> None:
        """Prints all values of this object"""
        packet = self
        print(f"ProtocolVersion: {packet.ProtocolVersion}")
        print(f"SecurityKeyID: {packet.SecurityKeyID}")
        print(f"Prefix: {packet.Prefix}")
        print(f"Route: {packet.Route}")
        print(f"EncryptionAlg: {packet.EncryptionAlg}")
        print(f"Compression: {packet.Compression}")
        print(f"Priority: {packet.Priority}")
        print(f"HeaderLength: {packet.HeaderLength}")
        print(f"HeaderEncoding: {packet.HeaderEncoding}")
        print(f"FrameDataLength: {packet.FrameDataLength}")
        print(f"PacketIdentifier: {packet.PacketIdentifier}")
        print(f"PacketType: {packet.PacketType}")

        if packet.Route == "1":
            print(f"PeerAddress: {packet.PeerAddress}")
            print(f"RecipientAddress: {packet.RecipientAddress}")
            print(f"TimeToLive: {packet.TimeToLive}")

        print(f"HeaderCheckSum: {packet.HeaderCheckSum}")
        print(f"ServicesFrameDataCheckSum: {packet.ServicesFrameDataCheckSum}")
        
    
            