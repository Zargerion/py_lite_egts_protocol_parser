from crc import CRC

import numpy as np
import unittest

class CRCUnitTest(unittest.TestCase):
    def test_crc8(self):
        crc = CRC.crc8(b"123456789")
        check_val = np.uint8(0xF7)
        self.assertEqual(crc, check_val)

    def test_crc16(self):
        crc = CRC.crc16(b"123456789")
        check_val = np.uint16(0x29b1)
        self.assertEqual(crc, check_val)


if __name__ == "__main__":
    unittest.main()