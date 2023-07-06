from io import BytesIO
from struct import unpack

import numpy as np

from binary_data import BinaryData

class Package:
    def __init__(
        self,
        ProtocolVersion: np.uint8,
        SecurityKeyID: np.uint8,
        Prefix: str,
        Route: str,
        EncryptionAlg: str,
        Compression: str,
        Priority: str,
        HeaderLength: np.uint8,
        HeaderEncoding: np.uint8,
        FrameDataLength: np.uint16,
        PacketIdentifier: np.uint16,
        PacketType: np.uint8,
        PeerAddress: np.uint16,
        RecipientAddress: np.uint16,
        TimeToLive: np.uint8,
        HeaderCheckSum: np.uint8,
        ServicesFrameData: BinaryData,
        ServicesFrameDataCheckSum: np.uint16
    ):
        self.ProtocolVersion = ProtocolVersion
        self.SecurityKeyID = SecurityKeyID
        self.Prefix = Prefix
        self.Route = Route
        self.EncryptionAlg = EncryptionAlg
        self.Compression = Compression
        self.Priority = Priority
        self.HeaderLength = HeaderLength
        self.HeaderEncoding = HeaderEncoding
        self.FrameDataLength = FrameDataLength
        self.PacketIdentifier = PacketIdentifier
        self.PacketType = PacketType
        self.PeerAddress = PeerAddress
        self.RecipientAddress = RecipientAddress
        self.TimeToLive = TimeToLive
        self.HeaderCheckSum = HeaderCheckSum
        self.ServicesFrameData = ServicesFrameData
        self.ServicesFrameDataCheckSum = ServicesFrameDataCheckSum

    def decode(self, content, options=None):
        if options is None:
            options = {}
        secret_key = options.get('secret', None)

        buf = BytesIO(content)
        p = Package()
        p.protocol_version = unpack('<B', buf.read(1))[0]
        p.security_key_id = unpack('<B', buf.read(1))[0]

        # parse flags
        flags = unpack('<B', buf.read(1))[0]
        flag_bits = f"{flags:08b}"
        p.prefix = flag_bits[:2]
        p.route = flag_bits[2:3]
        p.encryption_alg = flag_bits[3:5]
        p.compression = flag_bits[5:6]
        p.priority = flag_bits[6:]

        is_encrypted = p.encryption_alg != "00"

        p.header_length = unpack('<B', buf.read(1))[0]
        p.header_encoding = unpack('<B', buf.read(1))[0]

        p.frame_data_length = unpack('<H', buf.read(2))[0]
        p.packet_identifier = unpack('<H', buf.read(2))[0]

        p.packet_type = unpack('<B', buf.read(1))[0]

        if p.route == "1":
            p.peer_address = unpack('<H', buf.read(2))[0]
            p.recipient_address = unpack('<H', buf.read(2))[0]
            p.time_to_live = unpack('<B', buf.read(1))[0]

        p.header_check_sum = unpack('<B', buf.read(1))[0]

        data_frame_bytes = buf.read(p.frame_data_length)
        
        if p.packet_type == PtAppdataPacket:
            p.services_frame_data = ServiceDataSet()
        elif p.packet_type == PtResponsePacket:
            p.services_frame_data = PtResponse()
        
        if is_encrypted:
            if secret_key is None:
                raise Exception("Secret key is required for decryption")
            data_frame_bytes, err = secret_key.decode(data_frame_bytes)
            if err:
                raise Exception("Decryption error")

        err = p.services_frame_data.decode(data_frame_bytes)
        if err:
            raise Exception("Decryption error")
