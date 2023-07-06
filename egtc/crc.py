import numpy as np

class CRC:
    @staticmethod
    def crc8(data) -> np.uint8:
        """Needs to calculate Header checksum of package"""
        crc = np.uint8(0xFF)
        for b in data:
            crc ^= np.uint8(b)

            for _ in range(8):
                if crc & 0x80 != 0:
                    crc = (np.uint8(crc) << np.uint8(1)) ^ 0x31
                else:
                    crc = np.uint8(crc) << np.uint8(1)

        return crc

    @staticmethod
    def crc16(data) -> np.uint16:
        """Needs to calculate ServicesFrameDataCheckSum checksum of package"""
        crc = np.uint16(0xFFFF)
        for b in data:
            crc ^= np.uint16(b) << np.uint16(8)

            for _ in range(8):
                if crc & 0x8000 != 0:
                    crc = (np.uint16(crc) << np.uint8(1)) ^ 0x1021
                else:
                    crc = np.uint16(crc) << np.uint8(1)

        return crc

